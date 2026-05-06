"""CLI interface for the Logicbroker support agent."""

import argparse
import asyncio
import json
import logging
import sys
import textwrap

from dotenv import load_dotenv

from logicbroker_agent.graph import run_agent


def format_answer(result: dict, verbose: bool) -> str:
    """Format the agent result for terminal output."""
    lines = []

    if verbose:
        lines.append(f"Category:   {result['query_type']} ({result['query_confidence']:.0%} confidence)")
        if result["retry_count"] > 0:
            lines.append(f"Retries:    {result['retry_count']}")
        lines.append(f"Grounded:   {'yes' if result['grounded'] else 'no'}")
        lines.append(f"Docs used:  {len(result['relevant_documents'])}")
        lines.append("")

    # Answer body — wrap to terminal width
    wrapped = textwrap.fill(result["answer"], width=80)
    lines.append(wrapped)

    # Sources
    if result["sources"]:
        lines.append("")
        lines.append("Sources:")
        for i, src in enumerate(result["sources"], 1):
            lines.append(f"  [{i}] {src['title']}")
            lines.append(f"      {src['url']}")

    if verbose and result["documents"]:
        lines.append("")
        lines.append("Retrieval details:")
        for doc in result["documents"]:
            chunk = doc["chunk"]
            icon = "+" if doc["relevant"] else "-"
            score = f"[{chunk['score']:.3f}]" if "score" in chunk else ""
            lines.append(f"  {icon} {score} {chunk['title']} (chunk {chunk['chunk_index'] + 1})")
            if doc["reasoning"]:
                lines.append(f"    {doc['reasoning'][:100]}")

    return "\n".join(lines)


def format_json(result: dict, pretty: bool = False) -> str:
    """Format the agent result as JSON."""
    payload = {
        "query": result["query"],
        "classification": result["query_type"],
        "confidence": result["query_confidence"],
        "answer": result["answer"],
        "sources": result["sources"],
        "grounded": result["grounded"],
    }
    return json.dumps(payload, indent=2 if pretty else None)


def _repl(verbose: bool, as_json: bool = False, pretty: bool = False) -> None:
    """Interactive prompt loop."""
    print("Logicbroker Agent — interactive mode (type 'exit' or Ctrl-D to quit)\n")
    while True:
        try:
            query = input("ask> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            break
        if not as_json and verbose:
            print(f"\nQuery: {query}\n")
        result = asyncio.run(run_agent(query))
        if as_json:
            print(format_json(result, pretty=pretty))
        else:
            print(f"\n{format_answer(result, verbose=verbose)}\n")


def _output(result: dict, verbose: bool, as_json: bool, pretty: bool = False) -> None:
    """Print a single query result in the requested format."""
    if as_json:
        print(format_json(result, pretty=pretty))
    else:
        print(format_answer(result, verbose=verbose))


def main():
    parser = argparse.ArgumentParser(
        description="Logicbroker support agent — ask questions about the platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s                          interactive mode
              %(prog)s "How do I set up EDI?"    single query
              %(prog)s -v "Order API endpoints?" verbose output
              echo "How does the portal work?" | %(prog)s
        """),
    )
    parser.add_argument("query", nargs="*", help="The question to ask (reads from stdin if omitted)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show pipeline internals")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output (implies --json)")
    args = parser.parse_args()

    if args.pretty:
        args.json_output = True

    load_dotenv()

    # Configure logging — only show our agent logs in verbose mode, suppress noisy libraries
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        for noisy in ("httpx", "httpcore", "chromadb", "sentence_transformers", "urllib3"):
            logging.getLogger(noisy).setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Resolve query from args or stdin
    if args.query:
        query = " ".join(args.query)
        if not query:
            parser.error("Empty query.")
        if not args.json_output and args.verbose:
            print(f"Query: {query}\n")
        result = asyncio.run(run_agent(query))
        _output(result, verbose=args.verbose, as_json=args.json_output, pretty=args.pretty)
    elif not sys.stdin.isatty():
        query = sys.stdin.read().strip()
        if not query:
            parser.error("Empty query.")
        if not args.json_output and args.verbose:
            print(f"Query: {query}\n")
        result = asyncio.run(run_agent(query))
        _output(result, verbose=args.verbose, as_json=args.json_output, pretty=args.pretty)
    else:
        _repl(args.verbose, as_json=args.json_output, pretty=args.pretty)


if __name__ == "__main__":
    main()
