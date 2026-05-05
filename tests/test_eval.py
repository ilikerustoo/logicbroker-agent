"""Evaluation suite for the Logicbroker RAG agent.

Runs real queries through the pipeline and checks structural properties:
- Classification accuracy (correct category)
- Retrieval quality (sources found, relevant docs graded)
- Generation quality (key terms present, citations included)
- Grounding (hallucination check passes)

Requires ANTHROPIC_API_KEY. Skip with: pytest -m "not eval"
"""

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from logicbroker_agent.graph import run_agent

logger = logging.getLogger(__name__)

# Mark all tests in this module as eval (slow, requires API key)
pytestmark = pytest.mark.eval


@dataclass
class EvalCase:
    """A single evaluation case."""

    query: str
    expected_category: str
    expected_terms: list[str] = field(default_factory=list)
    expect_grounded: bool = True
    expect_sources: bool = True
    description: str = ""


EVAL_CASES = [
    # --- Onboarding ---
    EvalCase(
        query="How do I onboard a new trading partner in Logicbroker?",
        expected_category="onboarding",
        expected_terms=["partner", "portal"],
        description="Basic onboarding flow",
    ),
    EvalCase(
        query="What are the steps to get started with Logicbroker?",
        expected_category="onboarding",
        expected_terms=["account", "setup"],
        description="Getting started",
    ),
    # --- Order lifecycle ---
    EvalCase(
        query="How does the order lifecycle work in Logicbroker?",
        expected_category="order-lifecycle",
        expected_terms=["order"],
        description="Order lifecycle overview",
    ),
    EvalCase(
        query="How do I send a shipment confirmation?",
        expected_category="order-lifecycle",
        expected_terms=["shipment"],
        description="Shipment confirmation flow",
    ),
    EvalCase(
        query="How do returns work in Logicbroker?",
        expected_category="order-lifecycle",
        expected_terms=["return"],
        description="Returns process",
    ),
    # --- EDI/Technical ---
    EvalCase(
        query="How do I set up AS2 connectivity with Logicbroker?",
        expected_category="edi-technical",
        expected_terms=["AS2"],
        description="AS2 setup",
    ),
    EvalCase(
        query="What EDI document types does Logicbroker support?",
        expected_category="edi-technical",
        expected_terms=["EDI"],
        description="EDI document types",
    ),
    # --- API integration ---
    EvalCase(
        query="How do I authenticate with the Logicbroker API?",
        expected_category="api-integration",
        expected_terms=["API", "key"],
        description="API authentication",
    ),
    EvalCase(
        query="How do I create an order via the Logicbroker REST API?",
        expected_category="api-integration",
        expected_terms=["API", "order"],
        description="API order creation",
    ),
    # --- Platform config ---
    EvalCase(
        query="How do I set up automation rules in Logicbroker?",
        expected_category="platform-config",
        expected_terms=["automation", "rule"],
        description="Automation rules",
    ),
    EvalCase(
        query="How do I configure webhooks in Logicbroker?",
        expected_category="platform-config",
        expected_terms=["webhook"],
        description="Webhook configuration",
    ),
    # --- Edge cases ---
    EvalCase(
        query="What is the meaning of life?",
        expected_category="general",
        expected_terms=[],
        expect_grounded=False,
        expect_sources=False,
        description="Off-topic query should decline or give minimal answer",
    ),
    EvalCase(
        query="How do I configure inventory syncing with Logicbroker?",
        expected_category="platform-config",
        expected_terms=["inventory"],
        description="Inventory management",
    ),
]


@dataclass
class EvalResult:
    """Result of evaluating a single case."""

    case: EvalCase
    passed: bool
    category_correct: bool
    terms_found: list[str]
    terms_missing: list[str]
    grounded: bool
    has_sources: bool
    answer_length: int
    duration_secs: float
    error: str = ""


def evaluate_case(case: EvalCase) -> EvalResult:
    """Run a single eval case and check properties."""
    start = time.time()
    try:
        state = run_agent(case.query)
    except Exception as e:
        return EvalResult(
            case=case,
            passed=False,
            category_correct=False,
            terms_found=[],
            terms_missing=case.expected_terms,
            grounded=False,
            has_sources=False,
            answer_length=0,
            duration_secs=time.time() - start,
            error=str(e),
        )

    duration = time.time() - start
    answer_lower = state["answer"].lower()

    # Check classification
    category_correct = state["query_type"] == case.expected_category

    # Check expected terms in answer
    terms_found = [t for t in case.expected_terms if t.lower() in answer_lower]
    terms_missing = [t for t in case.expected_terms if t.lower() not in answer_lower]

    # Check grounding
    grounded = state["grounded"]

    # Check sources
    has_sources = len(state["sources"]) > 0

    # Determine pass/fail
    checks = [category_correct]
    if case.expected_terms:
        # Pass if at least half the expected terms appear
        checks.append(len(terms_found) >= len(case.expected_terms) / 2)
    if case.expect_grounded:
        checks.append(grounded)
    if case.expect_sources:
        checks.append(has_sources)

    passed = all(checks)

    return EvalResult(
        case=case,
        passed=passed,
        category_correct=category_correct,
        terms_found=terms_found,
        terms_missing=terms_missing,
        grounded=grounded,
        has_sources=has_sources,
        answer_length=len(state["answer"]),
        duration_secs=duration,
    )


def format_result(r: EvalResult) -> str:
    """Format a single result for display."""
    status = "PASS" if r.passed else "FAIL"
    parts = [
        f"[{status}] {r.case.description}",
        f"  Query: {r.case.query}",
        f"  Category: {'OK' if r.category_correct else 'WRONG'} "
        f"(expected {r.case.expected_category})",
        f"  Grounded: {r.grounded}",
        f"  Sources: {r.has_sources}",
        f"  Answer length: {r.answer_length} chars",
        f"  Duration: {r.duration_secs:.1f}s",
    ]
    if r.terms_missing:
        parts.append(f"  Missing terms: {r.terms_missing}")
    if r.error:
        parts.append(f"  Error: {r.error}")
    return "\n".join(parts)


# --- Pytest test cases ---


@pytest.fixture(scope="module")
def eval_results():
    """Run all eval cases once and share results across tests."""
    results = []
    for case in EVAL_CASES:
        result = evaluate_case(case)
        logger.info(format_result(result))
        results.append(result)

    # Write results to JSON for later analysis
    output_path = Path("tests/eval_results.json")
    output_path.write_text(json.dumps(
        [
            {
                "query": r.case.query,
                "description": r.case.description,
                "passed": r.passed,
                "category_correct": r.category_correct,
                "expected_category": r.case.expected_category,
                "terms_found": r.terms_found,
                "terms_missing": r.terms_missing,
                "grounded": r.grounded,
                "has_sources": r.has_sources,
                "answer_length": r.answer_length,
                "duration_secs": round(r.duration_secs, 1),
                "error": r.error,
            }
            for r in results
        ],
        indent=2,
    ))

    return results


def test_classification_accuracy(eval_results):
    """At least 80% of queries should be classified correctly."""
    correct = sum(1 for r in eval_results if r.category_correct)
    total = len(eval_results)
    accuracy = correct / total
    assert accuracy >= 0.8, (
        f"Classification accuracy {accuracy:.0%} ({correct}/{total}) below 80% threshold"
    )


def test_grounding_rate(eval_results):
    """At least 70% of expected-grounded queries should pass hallucination check."""
    groundable = [r for r in eval_results if r.case.expect_grounded]
    grounded = sum(1 for r in groundable if r.grounded)
    total = len(groundable)
    rate = grounded / total if total else 1.0
    assert rate >= 0.7, (
        f"Grounding rate {rate:.0%} ({grounded}/{total}) below 70% threshold"
    )


def test_source_retrieval(eval_results):
    """Queries expecting sources should have at least one."""
    expecting_sources = [r for r in eval_results if r.case.expect_sources]
    with_sources = sum(1 for r in expecting_sources if r.has_sources)
    total = len(expecting_sources)
    rate = with_sources / total if total else 1.0
    assert rate >= 0.9, (
        f"Source retrieval rate {rate:.0%} ({with_sources}/{total}) below 90% threshold"
    )


def test_term_coverage(eval_results):
    """At least 70% of queries should hit at least half their expected terms."""
    cases_with_terms = [r for r in eval_results if r.case.expected_terms]
    passing = sum(
        1
        for r in cases_with_terms
        if len(r.terms_found) >= len(r.case.expected_terms) / 2
    )
    total = len(cases_with_terms)
    rate = passing / total if total else 1.0
    assert rate >= 0.7, (
        f"Term coverage {rate:.0%} ({passing}/{total}) below 70% threshold"
    )


def test_offtopic_handling(eval_results):
    """Off-topic queries should either decline, produce a short answer, or pivot to Logicbroker content."""
    offtopic = [r for r in eval_results if r.case.expected_category == "general"]
    for r in offtopic:
        # Acceptable outcomes:
        # 1. Not grounded (declined)
        # 2. Short answer (< 500 chars)
        # 3. Grounded with sources (agent pivoted to relevant Logicbroker content — fine)
        is_acceptable = not r.grounded or r.answer_length < 500 or (r.grounded and r.has_sources)
        assert is_acceptable, (
            f"Off-topic query '{r.case.query}' produced a long ungrounded answer "
            f"without sources ({r.answer_length} chars)"
        )


def test_overall_pass_rate(eval_results):
    """At least 70% of all eval cases should pass all their checks."""
    passing = sum(1 for r in eval_results if r.passed)
    total = len(eval_results)
    rate = passing / total
    assert rate >= 0.7, (
        f"Overall pass rate {rate:.0%} ({passing}/{total}) below 70% threshold"
    )


def test_eval_summary(eval_results):
    """Print eval summary (always passes — informational)."""
    total = len(eval_results)
    passed = sum(1 for r in eval_results if r.passed)
    avg_duration = sum(r.duration_secs for r in eval_results) / total

    print("\n" + "=" * 60)
    print("EVAL SUMMARY")
    print("=" * 60)
    print(f"Total cases:  {total}")
    print(f"Passed:       {passed}/{total} ({passed / total:.0%})")
    print(f"Avg duration: {avg_duration:.1f}s per query")
    print()

    for r in eval_results:
        print(format_result(r))
        print()

    print("=" * 60)
