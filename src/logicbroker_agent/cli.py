"""CLI interface for the Logicbroker support agent."""

import argparse
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


def _repl(verbose: bool) -> None:
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
        if verbose:
            print(f"\nQuery: {query}\n")
        result = run_agent(query)
        print(f"\n{format_answer(result, verbose=verbose)}\n")


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
    args = parser.parse_args()

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
        if args.verbose:
            print(f"Query: {query}\n")
        result = run_agent(query)
        print(format_answer(result, verbose=args.verbose))
    elif not sys.stdin.isatty():
        query = sys.stdin.read().strip()
        if not query:
            parser.error("Empty query.")
        if args.verbose:
            print(f"Query: {query}\n")
        result = run_agent(query)
        print(format_answer(result, verbose=args.verbose))
    else:
        _repl(args.verbose)


if __name__ == "__main__":
    main()
