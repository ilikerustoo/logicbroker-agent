"""LangGraph adaptive RAG agent for Logicbroker support queries."""

import logging
import operator
import re
from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from logicbroker_agent.retriever import KnowledgeGraphRetriever, LogicbrokerRetriever, RetrievedChunk

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
    """Relevance grade for a single document chunk."""

    index: int = Field(description="The 0-based index of the document being graded")
    relevant: bool = Field(description="Whether this chunk is relevant to the query")
    reasoning: str = Field(description="Brief explanation of the relevance judgment")


class BatchDocumentGrades(BaseModel):
    """Batch relevance grades for all retrieved documents."""

    grades: list[DocumentGrade] = Field(description="One grade per document, in order")


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

    reasoning: str = Field(description="Brief explanation of grounding assessment")
    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="List of specific fabricated claims not in the sources (empty if none)",
    )
    grounded: bool = Field(
        description="Set to true unless the answer fabricates facts not in the sources. "
        "Omissions, simplifications, and minor imprecisions are NOT fabrications — set true for those."
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


async def classify_query(state: AgentState) -> dict:
    """Classify the query into one of 6 support categories."""
    llm = _get_llm(temperature=0, max_tokens=256, model="claude-haiku-4-5-20251001")
    structured_llm = llm.with_structured_output(QueryClassification)

    result = await structured_llm.ainvoke([
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


# Categories that benefit from API doc retrieval
_API_CATEGORIES = {"api-integration", "order-lifecycle", "edi-technical"}

# Categories where KG edges add value (relationship/workflow questions)
_KG_CATEGORIES = {"order-lifecycle", "onboarding", "edi-technical"}


async def retrieve(state: AgentState) -> dict:
    """Retrieve relevant chunks from the vector store and knowledge graph.

    Uses classification-first routing:
    - API-related queries: dual retrieval from API docs + KB articles
    - Relational queries (order-lifecycle, onboarding, edi): also query KG for edges
    - Other queries: standard vector retrieval

    KG results are injected as a synthetic chunk so they flow through the same
    grading and generation pipeline as vector results.
    """
    retriever = _get_retriever()
    kg_retriever = _get_kg_retriever()
    query_type = state.get("query_type", "")

    if query_type in _API_CATEGORIES:
        # Dual retrieval: API docs + KB articles, merged by score
        api_chunks = retriever.query(state["query"], top_k=5, doc_type_filter="api_doc")
        kb_chunks = retriever.query(state["query"], top_k=5, doc_type_filter="kb_article")

        # Merge and sort by score, take top 8
        all_chunks = api_chunks + kb_chunks
        all_chunks.sort(key=lambda c: c.score, reverse=True)
        chunks = all_chunks[:8]

        logger.info(
            f"Routed retrieval ({query_type}): {len(api_chunks)} API + "
            f"{len(kb_chunks)} KB → {len(chunks)} merged"
        )
    else:
        chunks = retriever.query(state["query"], top_k=5)
        logger.info(f"Retrieved {len(chunks)} chunks")

    for c in chunks:
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

    # Hybrid: add KG context for relational query types
    if query_type in _KG_CATEGORIES and kg_retriever.node_count > 0:
        kg_results = kg_retriever.query(state["query"], max_results=20)
        if kg_results:
            kg_text = "Knowledge Graph relationships:\n" + "\n".join(f"• {r}" for r in kg_results)
            kg_chunk = {
                "text": kg_text,
                "title": "Knowledge Graph (entity relationships)",
                "source_url": "",
                "category": "knowledge_graph",
                "doc_type": "kg_edges",
                "chunk_index": 0,
                "total_chunks": 1,
                "score": 0.95,  # High score so it doesn't get filtered
            }
            doc_dicts.insert(0, kg_chunk)
            logger.info(f"KG retrieval: {len(kg_results)} relationships added")

    return {"documents": [{"chunk": d, "relevant": True, "reasoning": ""} for d in doc_dicts]}


async def grade_documents(state: AgentState) -> dict:
    """Grade all retrieved chunks for relevance in a single LLM call."""
    llm = _get_llm(temperature=0, max_tokens=1024, model="claude-haiku-4-5-20251001")
    structured_llm = llm.with_structured_output(BatchDocumentGrades)

    # Build a numbered list of all chunks for the LLM
    docs = state["documents"]
    chunk_descriptions = []
    for i, doc in enumerate(docs):
        chunk = doc["chunk"]
        chunk_descriptions.append(
            f"[Document {i}] (from '{chunk['title']}', chunk {chunk['chunk_index'] + 1}):\n{chunk['text']}"
        )
    all_chunks_text = "\n\n---\n\n".join(chunk_descriptions)

    result = await structured_llm.ainvoke([
        SystemMessage(content=(
            "You are a relevance grader for Logicbroker support documentation. "
            "Given a user query and a set of document chunks, determine if each chunk "
            "contains information relevant to answering the query.\n\n"
            "IMPORTANT: Default to RELEVANT. Mark a chunk irrelevant ONLY if it is "
            "completely unrelated to the query topic. If a chunk discusses ANY entity, "
            "concept, or process mentioned in the query — even from a different angle "
            "(API details, specifications, configuration) — it IS relevant.\n\n"
            "Return one grade per document, using the document's index (0-based)."
        )),
        HumanMessage(content=(
            f"Query: {state['query']}\n\n"
            f"Documents to grade:\n\n{all_chunks_text}"
        )),
    ])

    # Build a lookup from index to grade
    grade_lookup = {g.index: g for g in result.grades}

    graded = []
    for i, doc in enumerate(docs):
        chunk = doc["chunk"]
        grade = grade_lookup.get(i)
        is_relevant = grade.relevant if grade else True  # default relevant if LLM missed it
        reasoning = grade.reasoning if grade else "not graded"

        graded.append({
            "chunk": chunk,
            "relevant": is_relevant,
            "reasoning": reasoning,
        })

        relevance = "RELEVANT" if is_relevant else "IRRELEVANT"
        logger.info(f"  Grade: {relevance} — {chunk['title']} (chunk {chunk['chunk_index'] + 1})")

    relevant = [g for g in graded if g["relevant"]]
    logger.info(f"Grading: {len(relevant)}/{len(graded)} relevant")

    return {
        "documents": graded,
        "relevant_documents": [g["chunk"] for g in graded if g["relevant"]],
    }


async def rewrite_query(state: AgentState) -> dict:
    """Rewrite the query for better retrieval."""
    llm = _get_llm(temperature=0.3, max_tokens=256, model="claude-haiku-4-5-20251001")

    result = await llm.ainvoke([
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


async def generate(state: AgentState) -> dict:
    """Generate a citation-grounded answer from relevant documents.

    Uses plain text generation (not structured output) so that the server
    can stream tokens to the client as they arrive.  Citation metadata is
    extracted from [N] references in the answer text and mapped back to the
    known source documents.
    """
    relevant_docs = state["relevant_documents"]

    if not relevant_docs:
        return _decline_response("I don't have enough information in the Logicbroker documentation to answer that question accurately.")

    # Build context block with numbered sources
    context_parts = []
    source_index: dict[int, dict] = {}
    for i, doc in enumerate(relevant_docs, 1):
        context_parts.append(f"[Source {i}: {doc['title']}]\n{doc['text']}")
        source_index[i] = {
            "title": doc["title"],
            "url": doc["source_url"],
        }
    context_block = "\n\n---\n\n".join(context_parts)

    llm = _get_llm(temperature=0, max_tokens=1024)

    result = await llm.ainvoke([
        SystemMessage(content=(
            "You are a Logicbroker support agent. Answer the user's question using ONLY "
            "the provided source documents. Follow these rules strictly:\n\n"
            "1. Every factual claim must cite its source using [N] notation matching the source numbers.\n"
            "2. If the sources don't contain enough information to fully answer the question, "
            "say so explicitly rather than guessing.\n"
            "3. Be concise and direct. Don't repeat the question.\n\n"
            f"Source documents:\n\n{context_block}"
        )),
        HumanMessage(content=state["query"]),
    ])

    answer_text = result.content.strip()

    # Extract cited source indices from the answer and build deduplicated sources list
    cited_indices = sorted(set(int(m) for m in re.findall(r"\[(\d+)\]", answer_text)))
    resolved_sources = []
    seen_urls: set[str] = set()
    for idx in cited_indices:
        src = source_index.get(idx)
        if not src or src["url"] in seen_urls:
            continue
        seen_urls.add(src["url"])
        resolved_sources.append(src)

    logger.info(f"Generated answer with {len(resolved_sources)} citations")
    return {
        "answer": answer_text,
        "sources": resolved_sources,
    }


async def check_hallucination(state: AgentState) -> dict:
    """Verify the generated answer is grounded in the source documents."""
    relevant_docs = state["relevant_documents"]
    answer = state["answer"]

    # Build source text for verification
    source_text = "\n\n---\n\n".join(
        f"[{doc['title']}]\n{doc['text']}" for doc in relevant_docs
    )

    llm = _get_llm(temperature=0, max_tokens=2048)
    structured_llm = llm.with_structured_output(HallucinationVerdict)

    result = await structured_llm.ainvoke([
        SystemMessage(content=(
            "You are a hallucination detector. Given an answer and source documents, check for fabricated content.\n\n"
            "Mark as GROUNDED (the default) unless the answer clearly fabricates information:\n"
            "- Invents facts, numbers, or procedures that appear NOWHERE in the sources\n"
            "- Directly contradicts the sources on a key point\n\n"
            "The following are NOT hallucinations — mark these as GROUNDED:\n"
            "- Omitting conditions, caveats, or edge cases from the sources\n"
            "- Rephrasing, summarizing, or simplifying source content\n"
            "- Synthesizing a workflow or process from multiple source documents\n"
            "- Minor imprecisions in how a transition or status is described\n"
            "- Reasonable inferences that follow from the source content\n\n"
            "Be LENIENT. An incomplete answer is not a hallucinated answer. "
            "Only reject answers that introduce facts the sources do not support at all.\n\n"
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


# --- Shared LLM + Retriever singletons ---

_llm_cache: dict[tuple[str, float, int], ChatAnthropic] = {}
_retriever: LogicbrokerRetriever | None = None
_kg_retriever: KnowledgeGraphRetriever | None = None


def _get_llm(
    temperature: float = 0,
    max_tokens: int = 1024,
    model: str = "claude-sonnet-4-6",
) -> ChatAnthropic:
    """Return a cached LLM client keyed by (model, temperature, max_tokens).

    Avoids creating a new Anthropic HTTP client for every node invocation.
    """
    key = (model, temperature, max_tokens)
    if key not in _llm_cache:
        _llm_cache[key] = ChatAnthropic(
            model=model, temperature=temperature, max_tokens=max_tokens,
        )
    return _llm_cache[key]


def _get_retriever() -> LogicbrokerRetriever:
    global _retriever
    if _retriever is None:
        _retriever = LogicbrokerRetriever()
    return _retriever


def _get_kg_retriever() -> KnowledgeGraphRetriever:
    global _kg_retriever
    if _kg_retriever is None:
        _kg_retriever = KnowledgeGraphRetriever()
    return _kg_retriever


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


async def run_agent(query: str) -> AgentState:
    """Run the agent pipeline on a query and return final state."""
    graph = build_graph()
    return await graph.ainvoke({
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
