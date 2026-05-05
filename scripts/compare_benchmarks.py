#!/usr/bin/env python3
"""Compare benchmark results across retrieval strategies.

Loads result JSON files from the three benchmarks (hybrid, KG-only, OpenAI embeddings)
and produces a side-by-side comparison table.

Usage:
    python scripts/compare_benchmarks.py
    python scripts/compare_benchmarks.py --json
    python scripts/compare_benchmarks.py --category
"""

import argparse
import json
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "tests"

DEFAULT_FILES = {
    "Hybrid (baseline)": RESULTS_DIR / "benchmark_e2e_results.json",
    "KG Only": RESULTS_DIR / "results_kg_only.json",
    "OpenAI Embeddings": RESULTS_DIR / "results_openai.json",
}


def load_results(path: Path) -> dict | None:
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def print_summary_table(results: dict[str, dict]):
    """Print a side-by-side summary comparison."""
    names = list(results.keys())
    col_width = max(len(n) for n in names) + 2

    header = f"{'Metric':<25}" + "".join(f"{n:<{col_width}}" for n in names)
    sep = "-" * len(header)

    print("\n" + sep)
    print("BENCHMARK COMPARISON")
    print(sep)
    print(header)
    print(sep)

    metrics = [
        ("Fact Coverage", "fact_coverage"),
        ("Fact %", "fact_pct"),
        ("Classification Acc %", "classification_accuracy"),
        ("Grounding Rate %", "grounding_rate"),
        ("Avg Latency (s)", "avg_latency_secs"),
    ]

    for label, key in metrics:
        row = f"{label:<25}"
        for name in names:
            data = results[name]
            if data is None:
                row += f"{'(missing)':<{col_width}}"
            else:
                val = data["summary"].get(key, "N/A")
                if isinstance(val, float):
                    row += f"{val:<{col_width}.1f}"
                else:
                    row += f"{str(val):<{col_width}}"
        print(row)

    print(sep)


def print_category_breakdown(results: dict[str, dict]):
    """Print per-category fact coverage comparison."""
    names = list(results.keys())
    col_width = max(len(n) for n in names) + 2

    # Gather categories from first available result
    categories = {}
    for data in results.values():
        if data is None:
            continue
        for q in data["queries"]:
            cat = q["category"]
            if cat not in categories:
                categories[cat] = {"total_facts": 0}
            categories[cat]["total_facts"] += q["facts"]["total"]
        break

    print(f"\n{'Category':<20}" + "".join(f"{n:<{col_width}}" for n in names))
    print("-" * (20 + col_width * len(names)))

    for cat in sorted(categories.keys()):
        row = f"{cat:<20}"
        for name in names:
            data = results[name]
            if data is None:
                row += f"{'(missing)':<{col_width}}"
                continue
            found = sum(
                q["facts"]["found"]
                for q in data["queries"]
                if q["category"] == cat
            )
            total = sum(
                q["facts"]["total"]
                for q in data["queries"]
                if q["category"] == cat
            )
            pct = (found / total * 100) if total > 0 else 0
            row += f"{found}/{total} ({pct:.0f}%){'':<{col_width - len(f'{found}/{total} ({pct:.0f}%)')}}"
        print(row)


def print_per_query(results: dict[str, dict]):
    """Print per-query grounding comparison."""
    names = list(results.keys())

    # Get queries from first available
    queries = []
    for data in results.values():
        if data is not None:
            queries = data["queries"]
            break

    print(f"\n{'#':<4}{'Query':<70}" + "".join(f"{n[:12]:<14}" for n in names))
    print("-" * (74 + 14 * len(names)))

    for i, q in enumerate(queries):
        query_text = q["query"][:67] + "..." if len(q["query"]) > 67 else q["query"]
        row = f"{i+1:<4}{query_text:<70}"
        for name in names:
            data = results[name]
            if data is None:
                row += f"{'?':<14}"
                continue
            dq = data["queries"][i]
            facts = f"{dq['facts']['found']}/{dq['facts']['total']}"
            grounded = "✓" if dq.get("grounded") else "✗"
            row += f"{facts} {grounded:<10}"
        print(row)


def main():
    parser = argparse.ArgumentParser(description="Compare benchmark results")
    parser.add_argument("--json", action="store_true", help="Output raw JSON comparison")
    parser.add_argument("--category", action="store_true", help="Show per-category breakdown")
    parser.add_argument("--per-query", action="store_true", help="Show per-query comparison")
    parser.add_argument("files", nargs="*", help="Override result files (name:path pairs)")
    args = parser.parse_args()

    # Load results
    file_map = dict(DEFAULT_FILES)
    for f in args.files:
        if ":" in f:
            name, path = f.split(":", 1)
            file_map[name] = Path(path)

    results = {}
    for name, path in file_map.items():
        data = load_results(path)
        if data is not None:
            results[name] = data
        else:
            print(f"⚠ Missing: {path}", file=sys.stderr)

    if not results:
        print("No result files found. Run the benchmarks first.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        comparison = {
            name: data["summary"] for name, data in results.items()
        }
        print(json.dumps(comparison, indent=2))
        return

    print_summary_table(results)

    if args.category:
        print_category_breakdown(results)

    if args.per_query:
        print_per_query(results)

    if not args.category and not args.per_query:
        print("\nUse --category for per-category breakdown, --per-query for per-query detail.")


if __name__ == "__main__":
    main()
