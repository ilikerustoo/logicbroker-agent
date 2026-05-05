"""Parse Logicbroker OpenAPI specs into structured markdown files."""

import json
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

SPEC_URLS = {
    "v3": "https://commerceapi.io/swagger/docs/v3",
    "v2": "https://commerceapi.io/swagger/docs/v2",
    "v1": "https://commerceapi.io/swagger/docs/v1",
}
# Use v3 as the primary — most complete
PRIMARY_VERSION = "v3"
OUTPUT_DIR = Path("data/api_docs")


def _fetch_spec(url: str) -> dict:
    """Fetch and parse an OpenAPI spec."""
    client = httpx.Client(timeout=30, follow_redirects=True)
    resp = client.get(url)
    resp.raise_for_status()
    return json.loads(resp.text)


def _resolve_ref(ref: str, spec: dict) -> dict:
    """Resolve a $ref pointer in the spec."""
    parts = ref.lstrip("#/").split("/")
    node = spec
    for p in parts:
        node = node.get(p, {})
    return node


def _schema_to_text(schema: dict, spec: dict, indent: int = 0, seen: set | None = None) -> str:
    """Convert a JSON schema to a readable text description."""
    if seen is None:
        seen = set()

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref in seen:
            return "  " * indent + "(circular reference)\n"
        seen = seen | {ref}
        schema = _resolve_ref(ref, spec)

    schema_type = schema.get("type", "object")
    prefix = "  " * indent

    if schema_type == "array":
        items = schema.get("items", {})
        result = f"{prefix}array of:\n"
        result += _schema_to_text(items, spec, indent + 1, seen)
        return result

    if schema_type == "object" or "properties" in schema:
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        if not props:
            return f"{prefix}object\n"
        lines = []
        for name, prop in props.items():
            if "$ref" in prop:
                prop = _resolve_ref(prop["$ref"], spec)
            p_type = prop.get("type", "object")
            desc = prop.get("description", "")
            req = " (required)" if name in required else ""
            enum = prop.get("enum")
            enum_str = f" enum={enum}" if enum else ""
            lines.append(f"{prefix}- **{name}**: {p_type}{req}{enum_str}")
            if desc:
                lines.append(f"{prefix}  {desc}")
        return "\n".join(lines) + "\n"

    desc = schema.get("description", "")
    enum = schema.get("enum")
    enum_str = f" enum={enum}" if enum else ""
    return f"{prefix}{schema_type}{enum_str} {desc}\n"


def _format_parameters(params: list[dict], spec: dict) -> str:
    """Format endpoint parameters as markdown."""
    if not params:
        return ""

    lines = ["**Parameters:**\n"]
    for p in params:
        if "$ref" in p:
            p = _resolve_ref(p["$ref"], spec)
        name = p.get("name", "?")
        location = p.get("in", "?")
        required = p.get("required", False)
        p_type = p.get("type", p.get("schema", {}).get("type", "string"))
        desc = p.get("description", "")
        req = "required" if required else "optional"
        lines.append(f"- `{name}` ({location}, {p_type}, {req}): {desc}")

    return "\n".join(lines) + "\n"


def _format_endpoint(path: str, method: str, details: dict, spec: dict) -> str:
    """Format a single endpoint as markdown."""
    summary = details.get("summary", "")
    description = details.get("description", "")
    params = details.get("parameters", [])
    responses = details.get("responses", {})

    lines = [f"### `{method.upper()} {path}`\n"]
    if summary:
        lines.append(f"{summary}\n")
    if description and description != summary:
        lines.append(f"{description}\n")

    param_text = _format_parameters(params, spec)
    if param_text:
        lines.append(param_text)

    # Request body (Swagger 2.0 uses "parameters" with "in: body")
    body_params = [p for p in params if isinstance(p, dict) and p.get("in") == "body"]
    if body_params:
        body = body_params[0]
        schema = body.get("schema", {})
        lines.append("**Request Body:**\n")
        lines.append("```")
        lines.append(_schema_to_text(schema, spec).rstrip())
        lines.append("```\n")

    # Responses
    if responses:
        lines.append("**Responses:**\n")
        for code, resp in responses.items():
            resp_desc = resp.get("description", "")
            lines.append(f"- `{code}`: {resp_desc}")

    return "\n".join(lines) + "\n"


def parse_spec_to_files(output_dir: Path | None = None) -> dict:
    """Parse the OpenAPI spec and write per-tag markdown files.

    Returns summary dict.
    """
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Fetching OpenAPI spec from {SPEC_URLS[PRIMARY_VERSION]}")
    spec = _fetch_spec(SPEC_URLS[PRIMARY_VERSION])

    info = spec.get("info", {})
    base_path = spec.get("basePath", "")
    host = spec.get("host", "commerceapi.io")

    # Group endpoints by tag
    tag_endpoints: dict[str, list[tuple[str, str, dict]]] = {}
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            tags = details.get("tags", ["Uncategorized"])
            for tag in tags:
                tag_endpoints.setdefault(tag, []).append((path, method, details))

    files_written = 0
    for tag, endpoints in sorted(tag_endpoints.items()):
        slug = tag.lower().replace(" ", "-")
        out_path = output_dir / f"{slug}.md"

        frontmatter = (
            f"---\n"
            f"title: \"{tag} API\"\n"
            f"source_url: \"{SPEC_URLS[PRIMARY_VERSION]}\"\n"
            f"api_version: \"{PRIMARY_VERSION}\"\n"
            f"base_url: \"https://{host}{base_path}\"\n"
            f"endpoints_count: {len(endpoints)}\n"
            f"---\n\n"
        )

        body = f"# {tag} API\n\n"
        body += f"Base URL: `https://{host}{base_path}`\n\n"
        body += f"Endpoints: {len(endpoints)}\n\n---\n\n"

        for path, method, details in sorted(endpoints, key=lambda x: (x[0], x[1])):
            body += _format_endpoint(path, method, details, spec)
            body += "---\n\n"

        out_path.write_text(frontmatter + body, encoding="utf-8")
        logger.info(f"  Wrote {tag}: {len(endpoints)} endpoints → {out_path.name}")
        files_written += 1

    # Also save the raw spec for reference
    raw_path = output_dir / "_openapi_v3_raw.json"
    raw_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    summary = {
        "api_version": PRIMARY_VERSION,
        "total_tags": len(tag_endpoints),
        "total_endpoints": sum(len(eps) for eps in tag_endpoints.values()),
        "files_written": files_written,
        "output_dir": str(output_dir),
    }
    logger.info(
        f"API docs parsed: {summary['total_tags']} groups, "
        f"{summary['total_endpoints']} endpoints, {files_written} files"
    )
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    result = parse_spec_to_files()
    print(f"\nSummary: {result['total_tags']} groups, {result['total_endpoints']} endpoints")
    print(f"Output: {result['output_dir']}")
