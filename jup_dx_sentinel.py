#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.jup.ag"
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "jup-dx-sentinel/0.1 (+https://github.com/ramimbo/jup-dx-sentinel)",
}


def request_json(path, params=None, api_key=None):
    query = f"?{urlencode(params)}" if params else ""
    req = Request(f"{API_BASE}{path}{query}", headers=DEFAULT_HEADERS.copy())
    if api_key:
        req.add_header("x-api-key", api_key)
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {path}: {body[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error calling {path}: {exc}") from exc


def search_tokens(query, limit, api_key):
    # Quote manually because Jupiter's search endpoint accepts human search strings.
    path = f"/tokens/v2/search?query={quote(query)}"
    req = Request(f"{API_BASE}{path}", headers=DEFAULT_HEADERS.copy())
    if api_key:
        req.add_header("x-api-key", api_key)
    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from token search: {body[:500]}") from exc
    return data[:limit]


def fetch_prices(mints, api_key):
    if not mints:
        return {}
    return request_json("/price/v3", {"ids": ",".join(mints)}, api_key=api_key)


def fmt_money(value):
    if value is None:
        return "n/a"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:.4f}"


def fmt_pct(value):
    if value is None:
        return "n/a"
    return f"{value:+.2f}%"


def review_signals(token):
    audit = token.get("audit") or {}
    flags = []
    if audit.get("isSus"):
        flags.append("audit.isSus")
    if token.get("isVerified") is False:
        flags.append("unverified")
    if audit.get("mintAuthorityDisabled") is False:
        flags.append("mint authority enabled")
    if audit.get("freezeAuthorityDisabled") is False:
        flags.append("freeze authority enabled")
    top_holders = audit.get("topHoldersPercentage")
    if isinstance(top_holders, (int, float)) and top_holders > 50:
        flags.append(f"concentrated holders {top_holders:.1f}%")
    return ", ".join(flags) if flags else "none observed"


def build_markdown(query, tokens, prices, used_api_key):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Jupiter Token Snapshot",
        "",
        f"Generated: {now}",
        f"Query: `{query}`",
        f"Mode: {'API key' if used_api_key else 'keyless prototype'}",
        "",
        "| Symbol | Name | Verified | Organic | Liquidity | USD | 24h | Review Signals | Mint |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for token in tokens:
        mint = token.get("id", "")
        price = prices.get(mint, {})
        lines.append(
            "| {symbol} | {name} | {verified} | {organic} | {liquidity} | {usd} | {change} | {flags} | `{mint}` |".format(
                symbol=token.get("symbol") or "",
                name=(token.get("name") or "").replace("|", "\\|"),
                verified="yes" if token.get("isVerified") else "no",
                organic=f"{token.get('organicScore'):.1f}" if isinstance(token.get("organicScore"), (int, float)) else "n/a",
                liquidity=fmt_money(token.get("liquidity")),
                usd=fmt_money(price.get("usdPrice", token.get("usdPrice"))),
                change=fmt_pct(price.get("priceChange24h", (token.get("stats24h") or {}).get("priceChange"))),
                flags=review_signals(token).replace("|", "\\|"),
                mint=mint,
            )
        )
    lines.extend([
        "",
        "## Notes",
        "",
        "- Read-only integration: no wallet connection, signatures, swaps, or private keys.",
        "- Token search already includes rich metadata; Price API V3 is needed for a consistent current price payload.",
        "- Review signals are prompts for human inspection, not automatic scam or trade recommendations.",
        "- Keyless mode is enough for testing, but production usage should send `x-api-key`.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Create a Jupiter token quality snapshot.")
    parser.add_argument("--query", default="JUP", help="Token symbol, name, or mint to search.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum tokens to include.")
    parser.add_argument("--markdown", help="Optional markdown output path.")
    parser.add_argument("--json", action="store_true", help="Print raw combined JSON instead of markdown.")
    args = parser.parse_args()

    api_key = os.environ.get("JUP_API_KEY")
    tokens = search_tokens(args.query, max(1, min(args.limit, 20)), api_key)
    if not api_key:
        time.sleep(2.1)
    prices = fetch_prices([token["id"] for token in tokens if token.get("id")], api_key)

    if args.json:
        print(json.dumps({"tokens": tokens, "prices": prices}, indent=2))
        return

    output = build_markdown(args.query, tokens, prices, bool(api_key))
    if args.markdown:
        Path(args.markdown).write_text(output)
        print(f"Wrote {args.markdown}")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
