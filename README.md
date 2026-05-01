# Jup DX Sentinel

Small Jupiter Developer Platform experiment for the Superteam Earn agent-eligible bounty:

- Listing: https://superteam.fun/earn/listing/not-your-regular-bounty
- Goal: build a useful, low-risk tool and produce a specific developer experience report.

## What It Does

`jup_dx_sentinel.py` searches Jupiter Tokens API for a token query, fetches current prices from Price API V3, and generates a compact markdown snapshot with:

- verification status
- organic score
- liquidity
- 24 hour price change
- suspicious-token audit flags when available

The tool is intentionally read-only. It does not trade, sign transactions, use private keys, or connect a wallet.

## Run

Keyless mode works for prototyping, but is rate-limited. If a Jupiter API key is available, set it in `JUP_API_KEY`.

```bash
python3 jup_dx_sentinel.py --query JUP --limit 5 --markdown sample-output.md
```

With an API key:

```bash
JUP_API_KEY=... python3 jup_dx_sentinel.py --query SOL --limit 5 --markdown sample-output.md
```

## Why This Fits The Bounty

The project exercises the Developer Platform path that the bounty asks agents to test:

- Tokens API search and metadata
- Price API V3
- keyless prototyping versus API-key production flow
- a concrete DX report with specific friction notes

The first public version is deliberately small so the report can focus on real integration details rather than a broad unfinished app.
