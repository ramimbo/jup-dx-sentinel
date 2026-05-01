# Jupiter Developer Experience Report

Listing: https://superteam.fun/earn/listing/not-your-regular-bounty  
Project: Jup DX Sentinel  
Status: draft, built from keyless API access on 2026-05-01

## Summary

I built a read-only CLI that combines Jupiter Tokens API search with Price API V3 to generate a token-quality markdown snapshot. The implementation avoided wallet connection, private keys, swaps, signatures, or paid infrastructure, which made it safe to prototype quickly.

## Onboarding Timing

- Docs discovery to first successful API call: under 10 minutes.
- First useful combined output: roughly 25 minutes after locating the keyless API path.
- API key setup was not completed yet because it requires a Developer Platform account session. The docs say keyless requests are supported for prototyping, so I used that path first.

## What Worked

- `Accept: text/markdown` on documentation pages is very helpful for coding agents.
- The portal setup page clearly states that keyless requests can start immediately and that production requests should use `x-api-key`.
- Tokens API returns enough metadata to build a meaningful first artifact without extra RPC calls.
- Price API V3 has a simple query shape and a compact response.

## Friction Notes

- The bounty text points at `developers.jup.ag`, while many docs resolve canonically under `dev.jup.ag/docs`. That is workable, but it adds a small orientation cost when collecting source links for a report.
- The docs mention `llms.txt`, and several pages say to fetch `https://dev.jup.ag/docs/llms.txt`. The root `https://developers.jup.ag/llms.txt` returned 404 during testing. The canonical docs path should be made more prominent wherever agents are expected to start.
- Keyless access is useful, but the rate limit requires local throttling. A tiny "keyless mode" example that intentionally sleeps between calls would help agents avoid accidental 429s.
- Tokens search includes `usdPrice` and Price API also returns price data. The docs explain Price API as the price source of truth, but a short "when Tokens price is enough versus when to call Price V3" note would reduce ambiguity.
- Token audit fields are valuable but not fully explained on the main Tokens overview page. A field-level example for common warning flags would help UI builders present trust signals without overclaiming.
- Python's default `urllib` request signature was blocked by Cloudflare 1010 even though the same endpoint worked through `curl`. Adding a descriptive `User-Agent` fixed this, but an agent-focused troubleshooting note would save time.

## API Details Exercised

- `GET https://api.jup.ag/tokens/v2/search?query=JUP`
- `GET https://api.jup.ag/price/v3?ids=<mint1>,<mint2>`

## Suggested Platform Improvements

- Put the agent-first quickstart in one visible path: docs index, keyless call, API key setup, and one complete read-only sample.
- Add a recommended local environment variable convention such as `JUP_API_KEY` to every language example.
- Add a machine-readable endpoint catalog link beside each API overview page, not only in the broader docs index.
- Add explicit guidance for safe read-only prototyping versus transaction-building endpoints.

## Submission Readiness

To finish the bounty submission cleanly, the remaining operator-gated item is a Jupiter Developer Platform account/API key and the account email required by the listing. The project itself runs in keyless mode and can be published as a public GitHub repo immediately.
