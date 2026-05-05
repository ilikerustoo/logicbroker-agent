"""LangGraph adaptive RAG agent for Logicbroker support queries."""

import logging
import operator
from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from logicbroker_agent.retriever import LogicbrokerRetriever, RetrievedChunk

logger = logging.getLogger(__name__)

# Query categories
CATEGORIES = [
    "onboarding",
    "order-lifecycle",
    "edi-technical",
    "api-integration",
    "platform-config",
    "general",
]

MAX_RETRIES = 2


# --- Structured output schemas ---


class QueryClassification(BaseModel):
    """Classification of a support query."""

    category: Literal[
        "onboarding",
        "order-lifecycle",
        "edi-technical",
        "api-integration",
        "platform-config",
        "general",
    ] = Field(description="The support category this query belongs to")
    confidence: float = Field(
        description="Confidence score between 0 and 1", ge=0.0, le=1.0
    )


class DocumentGrade(BaseModel):
    """Relevance grade for a retrieved document chunk."""

    relevant: bool = Field(description="Whether this chunk is relevant to the query")
    reasoning: str = Field(description="Brief explanation of the relevance judgment")


class Citation(BaseModel):
    """A single citation referencing a source document."""

    source_title: str = Field(description="Title of the source article")
    source_url: str = Field(description="URL of the source article")


class GeneratedAnswer(BaseModel):
    """A citation-grounded answer to a support query."""

    answer: str = Field(
        description=(
            "The answer to the user's question with inline citations "
            "using [N] notation (e.g., [1], [2]) referencing the sources list"
        )
    )
    citations: list[Citation] = Field(
        description="Ordered list of cited sources — [1] maps to citations[0], etc."
    )


class HallucinationVerdict(BaseModel):
    """Verdict on whether an answer is grounded in the provided sources."""

    grounded: bool = Field(
        description="True if every factual claim in the answer is supported by the source documents"
    )
    reasoning: str = Field(description="Explanation of grounding assessment")
    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="List of specific claims not supported by the source documents",
    )


# --- Agent State ---


class GradedDocument(TypedDict):
    """A document chunk with its relevance grade."""

    chunk: dict  # serialized RetrievedChunk fields
    relevant: bool
    reasoning: str


class AgentState(TypedDict):
    """State flowing through the adaptive RAG graph."""

    query: str
    query_type: str
    query_confidence: float
    documents: list[GradedDocument]
    relevant_documents: list[dict]
    retry_count: int
    answer: str
    sources: list[dict]
    grounded: bool
    verbose: bool


# --- Node implementations ---


def classify_query(state: AgentState) -> dict:
    """Classify the query into one of 6 support categories."""
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=256)
    structured_llm = llm.with_structured_output(QueryClassification)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a query classifier for Logicbroker, a commerce orchestration platform. "
            "Classify the user's support query into exactly one category:\n"
            "- onboarding: setup, connection, partner configuration, getting started\n"
            "- order-lifecycle: orders, acknowledgements, shipments, invoices, returns\n"
            "- edi-technical: EDI/AS2/SFTP/VAN troubleshooting, document format issues\n"
            "- api-integration: developer API usage, authentication, endpoints\n"
            "- platform-config: automation rules, settings, reporting, user management\n"
            "- general: anything that doesn't fit the above categories"
        )),
        HumanMessage(content=state["query"]),
    ])

    logger.info(f"Classification: {result.category} (confidence: {result.confidence:.2f})")
    return {
        "query_type": result.category,
        "query_confidence": result.confidence,
    }


def retrieve(state: AgentState) -> dict:
    """Retrieve relevant chunks from the vector store."""
    retriever = _get_retriever()
    chunks = retriever.query(state["query"], top_k=5)

    logger.info(f"Retrieved {len(chunks)} chunks")
    for i, c in enumerate(chunks):
        logger.debug(f"  [{c.score:.3f}] {c.title} (chunk {c.chunk_index + 1})")

    # Convert to serializable dicts
    doc_dicts = [
        {
            "text": c.text,
            "title": c.title,
            "source_url": c.source_url,
            "category": c.category,
            "doc_type": c.doc_type,
            "chunk_index": c.chunk_index,
            "total_chunks": c.total_chunks,
            "score": c.score,
        }
        for c in chunks
    ]

    return {"documents": [{"chunk": d, "relevant": True, "reasoning": ""} for d in doc_dicts]}


def grade_documents(state: AgentState) -> dict:
    """Grade each retrieved chunk for relevance to the query."""
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=256)
    structured_llm = llm.with_structured_output(DocumentGrade)

    graded = []
    for doc in state["documents"]:
        chunk = doc["chunk"]
        result = structured_llm.invoke([
            SystemMessage(content=(
                "You are a relevance grader for Logicbroker support documentation. "
                "Given a user query and a document chunk, determine if the chunk "
                "contains information relevant to answering the query. "
                "Be generous — if the chunk is somewhat related, mark it relevant."
            )),
            HumanMessage(content=(
                f"Query: {state['query']}\n\n"
                f"Document chunk (from '{chunk['title']}'):\n{chunk['text']}"
            )),
        ])

        graded.append({
            "chunk": chunk,
            "relevant": result.relevant,
            "reasoning": result.reasoning,
        })

        relevance = "RELEVANT" if result.relevant else "IRRELEVANT"
        logger.info(f"  Grade: {relevance} — {chunk['title']} (chunk {chunk['chunk_index'] + 1})")

    relevant = [g for g in graded if g["relevant"]]
    logger.info(f"Grading: {len(relevant)}/{len(graded)} relevant")

    return {
        "documents": graded,
        "relevant_documents": [g["chunk"] for g in graded if g["relevant"]],
    }


def rewrite_query(state: AgentState) -> dict:
    """Rewrite the query for better retrieval."""
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.3, max_tokens=256)

    result = llm.invoke([
        SystemMessage(content=(
            "You are a query rewriter for Logicbroker support. "
            "The original query didn't retrieve relevant documents. "
            "Rewrite it to be more specific to Logicbroker's platform, "
            "using domain terminology (EDI, portal, documents, partners, etc.). "
            "Return ONLY the rewritten query, nothing else."
        )),
        HumanMessage(content=f"Original query: {state['query']}"),
    ])

    new_query = result.content.strip()
    logger.info(f"Query rewritten: '{state['query']}' → '{new_query}'")
    return {
        "query": new_query,
        "retry_count": state["retry_count"] + 1,
    }


def generate(state: AgentState) -> dict:
    """Generate a citation-grounded answer from relevant documents."""
    relevant_docs = state["relevant_documents"]

    if not relevant_docs:
        return _decline_response("I don't have enough information in the Logicbroker documentation to answer that question accurately.")

    # Build context block with numbered sources
    context_parts = []
    sources = []
    for i, doc in enumerate(relevant_docs, 1):
        context_parts.append(f"[Source {i}: {doc['title']}]\n{doc['text']}")
        sources.append({
            "index": i,
            "title": doc["title"],
            "url": doc["source_url"],
            "category": doc["category"],
        })
    context_block = "\n\n---\n\n".join(context_parts)

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=1024)
    structured_llm = llm.with_structured_output(GeneratedAnswer)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a Logicbroker support agent. Answer the user's question using ONLY "
            "the provided source documents. Follow these rules strictly:\n\n"
            "1. Every factual claim must cite its source using [N] notation matching the source numbers.\n"
            "2. If the sources don't contain enough information to fully answer the question, "
            "say so explicitly rather than guessing.\n"
            "3. Be concise and direct. Don't repeat the question.\n"
            "4. Use the source titles and URLs exactly as provided in your citations list.\n\n"
            f"Source documents:\n\n{context_block}"
        )),
        HumanMessage(content=state["query"]),
    ])

    # Map citations back to actual source metadata (LLM may mangle URLs)
    # Deduplicate by URL — multiple chunks from the same page should appear once
    source_lookup = {doc["title"]: doc for doc in relevant_docs}
    resolved_sources = []
    seen_urls = set()
    for c in result.citations:
        matched_doc = source_lookup.get(c.source_title)
        url = matched_doc["source_url"] if matched_doc else c.source_url
        if url in seen_urls:
            continue
        seen_urls.add(url)
        resolved_sources.append({"title": c.source_title, "url": url})

    logger.info(f"Generated answer with {len(result.citations)} citations")
    return {
        "answer": result.answer,
        "sources": resolved_sources,
    }


def check_hallucination(state: AgentState) -> dict:
    """Verify the generated answer is grounded in the source documents."""
    relevant_docs = state["relevant_documents"]
    answer = state["answer"]

    # Build source text for verification
    source_text = "\n\n---\n\n".join(
        f"[{doc['title']}]\n{doc['text']}" for doc in relevant_docs
    )

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=512)
    structured_llm = llm.with_structured_output(HallucinationVerdict)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a hallucination detector. Given an answer and the source documents it claims to be based on, "
            "determine whether every factual claim in the answer is supported by the sources.\n\n"
            "Mark as NOT grounded if the answer:\n"
            "- Contains specific facts, numbers, or procedures not in the sources\n"
            "- Makes claims that contradict the sources\n"
            "- Presents speculation or general knowledge as if it came from the sources\n\n"
            "Mark as grounded if:\n"
            "- All factual claims are directly supported by source text\n"
            "- The answer only synthesizes and rephrases information from the sources\n"
            "- Hedged statements ('the docs don't cover this') are acceptable\n\n"
            f"Source documents:\n\n{source_text}"
        )),
        HumanMessage(content=f"Answer to verify:\n\n{answer}"),
    ])

    logger.info(f"Hallucination check: {'GROUNDED' if result.grounded else 'NOT GROUNDED'} — {result.reasoning}")
    if result.unsupported_claims:
        for claim in result.unsupported_claims:
            logger.info(f"  Unsupported: {claim}")

    if result.grounded:
        return {"grounded": True}

    # Answer failed grounding — replace with decline
    logger.info("Replacing ungrounded answer with decline response")
    return _decline_response(
        "I found some related documentation, but I'm not confident I can answer this accurately "
        "based on what's available. Please contact Logicbroker support for assistance."
    )


def _decline_response(message: str) -> dict:
    """Build a standard decline response."""
    return {
        "answer": message,
        "sources": [],
        "grounded": False,
    }


# --- Routing functions ---


def route_after_grading(state: AgentState) -> Literal["generate", "rewrite_query"]:
    """Decide whether to generate or rewrite based on grading results."""
    relevant = [d for d in state["documents"] if d["relevant"]]

    if relevant:
        return "generate"

    if state["retry_count"] < MAX_RETRIES:
        logger.info(f"No relevant docs, rewriting (attempt {state['retry_count'] + 1}/{MAX_RETRIES})")
        return "rewrite_query"

    # No relevant docs after exhausting retries — generate will produce a decline
    logger.info("No relevant docs after max retries, generating decline response")
    return "generate"


def route_after_hallucination_check(state: AgentState) -> Literal["__end__"]:
    """After hallucination check, always proceed to END.

    The check_hallucination node already replaces ungrounded answers
    with a decline response, so no further routing is needed.
    """
    return "__end__"


# --- Retriever singleton ---

_retriever: LogicbrokerRetriever | None = None


def _get_retriever() -> LogicbrokerRetriever:
    global _retriever
    if _retriever is None:
        _retriever = LogicbrokerRetriever()
    return _retriever


# --- Graph builder ---


def build_graph() -> StateGraph:
    """Build and compile the adaptive RAG graph.

    Flow: classify → retrieve → grade → (generate → hallucination_check → END | rewrite → retrieve)
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("classify", classify_query)
    graph.add_node("retrieve", retrieve)
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("rewrite_query", rewrite_query)
    graph.add_node("generate", generate)
    graph.add_node("check_hallucination", check_hallucination)

    # Wire edges
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "grade_documents")
    graph.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "generate": "generate",
            "rewrite_query": "rewrite_query",
        },
    )
    graph.add_edge("rewrite_query", "retrieve")
    graph.add_edge("generate", "check_hallucination")
    graph.add_edge("check_hallucination", END)

    return graph.compile()


def run_agent(query: str) -> AgentState:
    """Run the agent pipeline on a query and return final state."""
    graph = build_graph()
    return graph.invoke({
        "query": query,
        "query_type": "",
        "query_confidence": 0.0,
        "documents": [],
        "relevant_documents": [],
        "retry_count": 0,
        "answer": "",
        "sources": [],
        "grounded": False,
        "verbose": False,
    })
