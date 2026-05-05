"""FastAPI server with SSE streaming for the Logicbroker agent."""

__version__ = "0.1.2"

import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from logicbroker_agent.graph import build_graph

logger = logging.getLogger(__name__)

# Module-level graph instance, warmed at startup
_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm the graph and retriever weights at startup."""
    global _graph
    logger.info("Warming graph and embedding model weights...")
    _graph = build_graph()
    # Force retriever + embedding model initialization by running a dummy query
    from logicbroker_agent.graph import _get_retriever, _get_kg_retriever
    _get_retriever().query("warmup", top_k=1)
    _get_kg_retriever()
    logger.info("Model weights loaded, ready to serve.")
    yield


app = FastAPI(title="Logicbroker Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    query: str


def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


_NODE_LABELS = {
    "classify": ("classify_query", "classifying query"),
    "retrieve": ("retrieve", "searching knowledge base"),
    "grade_documents": ("grade_documents", "grading document relevance"),
    "rewrite_query": ("rewrite_query", "rewriting query for better retrieval"),
    "generate": ("generate", "composing answer"),
    "check_hallucination": ("check_hallucination", "verifying answer grounding"),
}


async def _stream_agent(query: str):
    """Run the agent graph with streaming, yielding SSE events per node."""
    graph = _graph or build_graph()

    initial_state = {
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
    }

    yield _sse_event("trace", {
        "kind": "shell",
        "text": f'$ logic-agent ask "{query}"',
    })
    yield _sse_event("trace", {
        "kind": "dim",
        "text": "loading knowledge base index...",
    })

    start = time.time()
    step_count = 0

    # Accumulate full state from stream deltas
    accumulated = dict(initial_state)

    try:
        async for chunk in graph.astream(initial_state):
            # LangGraph stream yields {node_name: state_update}
            for node_name, state_update in chunk.items():
                for key, value in state_update.items():
                    accumulated[key] = value

                if node_name not in _NODE_LABELS:
                    continue

                tool_name, description = _NODE_LABELS[node_name]
                step_count += 1

                yield _sse_event("trace", {
                    "kind": "step",
                    "tool": tool_name,
                    "arg": description,
                    "text": f"  {tool_name}({description})",
                })

                if node_name == "classify":
                    qtype = state_update.get("query_type", "")
                    conf = state_update.get("query_confidence", 0)
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f"  category: {qtype} (confidence: {conf:.2f})",
                    })

                elif node_name == "retrieve":
                    docs = state_update.get("documents", [])
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f"  {len(docs)} chunks retrieved",
                    })

                elif node_name == "grade_documents":
                    docs = state_update.get("documents", [])
                    relevant = [d for d in docs if d.get("relevant")]
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f"  {len(relevant)}/{len(docs)} relevant",
                    })

                elif node_name == "rewrite_query":
                    new_q = state_update.get("query", "")
                    retry = state_update.get("retry_count", 0)
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f'  rewritten (attempt {retry}): "{new_q[:80]}"',
                    })

                elif node_name == "generate":
                    sources = state_update.get("sources", [])
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f"  answer generated with {len(sources)} citations",
                    })

                elif node_name == "check_hallucination":
                    grounded = state_update.get("grounded", False)
                    verdict = "grounded" if grounded else "not grounded"
                    yield _sse_event("trace", {
                        "kind": "result",
                        "text": f"  verdict: {verdict}",
                    })

        elapsed = time.time() - start

        yield _sse_event("trace", {
            "kind": "ok",
            "text": f"  done in {elapsed:.1f}s  {step_count} steps",
        })

        yield _sse_event("answer", {
            "text": accumulated.get("answer", ""),
            "sources": [
                {"title": s.get("title", ""), "url": s.get("url", "")}
                for s in accumulated.get("sources", [])
            ],
            "grounded": accumulated.get("grounded", False),
        })

    except Exception as e:
        logger.exception("Agent execution failed")
        yield _sse_event("error", {"message": str(e)})

    yield _sse_event("done", {})


@app.post("/api/ask")
async def ask(req: AskRequest):
    return StreamingResponse(
        _stream_agent(req.query),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": __version__, "warm": _graph is not None}


# Serve static frontend if the build directory exists.
# Check relative to the module (dev) and relative to cwd (Docker).
_candidates = [
    Path(__file__).parent.parent.parent / "web" / "dist",
    Path.cwd() / "web" / "dist",
]
for _candidate in _candidates:
    if _candidate.exists():
        app.mount("/", StaticFiles(directory=str(_candidate), html=True), name="static")
        break
