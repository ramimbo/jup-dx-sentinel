#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = "jup-dx-sentinel-ai-probe/0.1 (+https://github.com/ramimbo/jup-dx-sentinel)"
DOCS_BASE = "https://developers.jup.ag"
API_BASE = "https://api.jup.ag"

DOC_TARGETS = {
    "llms.txt": f"{DOCS_BASE}/docs/llms.txt",
    "skill.md": f"{DOCS_BASE}/docs/skill.md",
    "ai-overview-md": f"{DOCS_BASE}/docs/ai.md",
    "tokens-md": f"{DOCS_BASE}/docs/tokens/token-information.md",
    "price-md": f"{DOCS_BASE}/docs/price/v3",
    "tokens-openapi": f"{DOCS_BASE}/docs/openapi-spec/tokens/v2/tokens.yaml",
    "price-openapi": f"{DOCS_BASE}/docs/openapi-spec/price/v3/price.yaml",
}


def fetch(url, accept=None):
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    req = Request(url, headers=headers)
    try:
        started = time.monotonic()
        with urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {
                "ok": True,
                "status": resp.status,
                "url": url,
                "final_url": resp.geturl(),
                "content_type": resp.headers.get("content-type", ""),
                "elapsed_ms": round((time.monotonic() - started) * 1000),
                "body": body,
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "url": url,
            "final_url": exc.geturl(),
            "content_type": exc.headers.get("content-type", ""),
            "elapsed_ms": None,
            "body": body,
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": "network-error",
            "url": url,
            "final_url": url,
            "content_type": "",
            "elapsed_ms": None,
            "body": str(exc),
        }


def api_json(path):
    result = fetch(f"{API_BASE}{path}", accept="application/json")
    if result["ok"]:
        try:
            result["json"] = json.loads(result["body"])
        except json.JSONDecodeError as exc:
            result["ok"] = False
            result["json_error"] = str(exc)
    return result


def npm_cli_info():
    if not shutil.which("npm"):
        return {"ok": False, "reason": "npm not installed"}
    proc = subprocess.run(
        ["npm", "view", "@jup-ag/cli", "version", "description", "dist-tags", "--json"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=25,
        check=False,
    )
    if proc.returncode != 0:
        return {"ok": False, "reason": proc.stderr.strip()[:500]}
    try:
        return {"ok": True, "metadata": json.loads(proc.stdout)}
    except json.JSONDecodeError:
        return {"ok": False, "reason": proc.stdout.strip()[:500]}


def summarize_docs(results):
    llms = results["docs"]["llms.txt"]["body"]
    skill = results["docs"]["skill.md"]["body"]
    markdown_pages = [name for name, value in results["docs"].items() if name.endswith("-md") and value["ok"]]
    openapi_specs = [name for name, value in results["docs"].items() if name.endswith("openapi") and value["ok"]]
    llms_links = re.findall(r"\]\((https://developers\.jup\.ag/[^)]+)\)", llms)
    return {
        "llms_link_count": len(llms_links),
        "llms_mentions_keyless": "Keyless access" in llms,
        "llms_mentions_cli": "@jup-ag/cli" in llms,
        "llms_mentions_mcp": "MCP" in llms,
        "llms_mentions_skills": "skills" in llms.lower(),
        "skill_line_count": len([line for line in skill.splitlines() if line.strip()]),
        "markdown_pages_ok": markdown_pages,
        "openapi_specs_ok": openapi_specs,
    }


def run_probe(query):
    docs = {}
    for name, url in DOC_TARGETS.items():
        accept = "text/markdown" if name.endswith("-md") or name == "price-md" else None
        docs[name] = fetch(url, accept=accept)

    token_result = api_json(f"/tokens/v2/search?query={query}")
    tokens = token_result.get("json") if isinstance(token_result.get("json"), list) else []
    mints = [token.get("id") for token in tokens[:5] if token.get("id")]
    time.sleep(2.1)
    price_result = api_json(f"/price/v3?ids={','.join(mints)}") if mints else {"ok": False, "body": "no mints"}

    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "query": query,
        "docs": docs,
        "summary": {},
        "api": {
            "tokens_search": token_result,
            "price_v3": price_result,
        },
        "cli": npm_cli_info(),
    }
    results["summary"] = summarize_docs(results)
    return results


def status_cell(result):
    if result["ok"]:
        return f"{result['status']} in {result['elapsed_ms']}ms"
    return str(result["status"])


def render_markdown(results):
    summary = results["summary"]
    token_json = results["api"]["tokens_search"].get("json")
    price_json = results["api"]["price_v3"].get("json")
    token_count = len(token_json) if isinstance(token_json, list) else 0
    price_count = len(price_json) if isinstance(price_json, dict) else 0
    cli = results["cli"]

    lines = [
        "# Jupiter AI Stack Probe",
        "",
        f"Generated: {results['generated_at']}",
        f"Token query: `{results['query']}`",
        "",
        "## Surface Checks",
        "",
        "| Surface | Status | Final URL | Content Type |",
        "| --- | ---: | --- | --- |",
    ]
    for name, result in results["docs"].items():
        lines.append(
            f"| `{name}` | {status_cell(result)} | {result['final_url']} | `{result['content_type']}` |"
        )

    lines.extend([
        "",
        "## Parsed Signals",
        "",
        f"- `llms.txt` linked documentation pages found: {summary['llms_link_count']}",
        f"- `llms.txt` mentions keyless access: {'yes' if summary['llms_mentions_keyless'] else 'no'}",
        f"- `llms.txt` mentions CLI: {'yes' if summary['llms_mentions_cli'] else 'no'}",
        f"- `llms.txt` mentions MCP: {'yes' if summary['llms_mentions_mcp'] else 'no'}",
        f"- `llms.txt` mentions skills: {'yes' if summary['llms_mentions_skills'] else 'no'}",
        f"- `skill.md` non-empty line count: {summary['skill_line_count']}",
        f"- Markdown docs fetched successfully: {', '.join(summary['markdown_pages_ok']) or 'none'}",
        f"- OpenAPI specs fetched successfully: {', '.join(summary['openapi_specs_ok']) or 'none'}",
        "",
        "## Read-Only API Smoke",
        "",
        f"- Tokens search status: {status_cell(results['api']['tokens_search'])}; returned {token_count} rows.",
        f"- Price V3 status: {status_cell(results['api']['price_v3'])}; returned {price_count} priced mints.",
    ])

    if cli["ok"]:
        metadata = cli["metadata"]
        lines.extend([
            "",
            "## CLI Registry Check",
            "",
            f"- `@jup-ag/cli` latest version: `{metadata.get('version')}`",
            f"- Description: {metadata.get('description')}",
        ])
    else:
        lines.extend(["", "## CLI Registry Check", "", f"- Unable to read npm metadata: {cli['reason']}"])

    lines.extend([
        "",
        "## DX Notes",
        "",
        "- The AI docs are genuinely useful as a starting map: `llms.txt` exposes keyless limits, portal setup, API families, and AI tooling in one file.",
        "- `skill.md` is reachable, but it is only a high-level pointer to the agent-skills repository. An inline list of available skill names and install commands would save an agent one extra hop.",
        "- The OpenAPI specs are easy to discover from `llms.txt`, but guessed shorter paths such as `/docs/openapi-spec/price/price.yaml` return 404. Agents should follow the exact spec links.",
        "- The docs export path works well with `.md` pages and `Accept: text/markdown`; `/docs/price/v3` redirects to the broader price markdown page, which is harmless but slightly surprising.",
        "- The npm package metadata is visible without installation, which is enough for safe agent discovery before any key, wallet, or trading command is configured.",
        "- This probe intentionally does not install the CLI, configure keys, connect a wallet, place orders, or call transaction-writing endpoints.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Probe Jupiter AI/docs surfaces for a DX report.")
    parser.add_argument("--query", default="JUP", help="Token query for read-only API smoke checks.")
    parser.add_argument("--markdown", help="Optional markdown output path.")
    parser.add_argument("--json", action="store_true", help="Print full JSON probe payload.")
    args = parser.parse_args()

    results = run_probe(args.query)
    if args.json:
        print(json.dumps(results, indent=2))
        return

    markdown = render_markdown(results)
    if args.markdown:
        Path(args.markdown).write_text(markdown)
        print(f"Wrote {args.markdown}")
    else:
        print(markdown, end="")


if __name__ == "__main__":
    main()
