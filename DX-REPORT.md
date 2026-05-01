# Jupiter Developer Experience Report

Listing: https://superteam.fun/earn/listing/not-your-regular-bounty  
Project: Jup DX Sentinel  
Status: draft, built from keyless API access and AI-stack probing on 2026-05-01

## Summary

I built a read-only CLI that combines Jupiter Tokens API search with Price API V3 to generate a token-quality markdown snapshot. I also added a second read-only probe that tests Jupiter's AI/docs surfaces: `llms.txt`, `skill.md`, Markdown export, OpenAPI spec links, and CLI package discovery.

The implementation avoided wallet connection, private keys, swaps, signatures, transaction-writing endpoints, or paid infrastructure, which made it safe to prototype quickly.

## Onboarding Timing

- Docs discovery to first successful API call: under 10 minutes.
- First useful combined output: roughly 25 minutes after locating the keyless API path.
- API key setup was not completed yet because it requires a Developer Platform account session. The docs say keyless requests are supported for prototyping, so I used that path first and throttled local requests.

## What Worked

- `Accept: text/markdown` on documentation pages is very helpful for coding agents.
- The portal setup page clearly states that keyless requests can start immediately and that production requests should use `x-api-key`.
- `llms.txt` was the best agent entry point. It exposed the API families, keyless rate limit, portal setup path, AI tooling, and exact OpenAPI spec links in one machine-readable file.
- Tokens API returns enough metadata to build a meaningful first artifact without extra RPC calls.
- Price API V3 has a simple query shape and a compact response.
- OpenAPI specs were directly fetchable when following exact links from `llms.txt`.

## AI Stack Probe Results

I added `jup_ai_stack_probe.py` and generated `AI-STACK-PROBE.md`.

- `https://developers.jup.ag/docs/llms.txt`: HTTP 200, 227 documentation links parsed.
- `https://developers.jup.ag/docs/skill.md`: HTTP 200, but only three non-empty content lines.
- Markdown docs export worked for AI overview, token information, and price docs.
- `https://developers.jup.ag/docs/openapi-spec/tokens/v2/tokens.yaml`: HTTP 200.
- `https://developers.jup.ag/docs/openapi-spec/price/v3/price.yaml`: HTTP 200.
- Read-only API smoke check returned 20 token search rows and five priced mints for `JUP`.
- `npm view @jup-ag/cli` returned `@jup-ag/cli` version `0.10.0` without installing or configuring the CLI.

## Friction Notes

- The bounty text points at `developers.jup.ag`, while many docs resolve canonically under `dev.jup.ag/docs`. That is workable, but it adds a small orientation cost when collecting source links for a report.
- The docs mention `llms.txt`, and several pages say to fetch `https://dev.jup.ag/docs/llms.txt`. The root `https://developers.jup.ag/llms.txt` returned 404 during testing. The canonical docs path should be made more prominent wherever agents are expected to start.
- `skill.md` is reachable, but it is only a pointer to the agent-skills repository. For agents, it would be more useful if it listed the available skill names, install commands, and short capability descriptions inline.
- OpenAPI spec paths are easy to use if copied from `llms.txt`, but guessed shorter paths such as `/docs/openapi-spec/price/price.yaml` and `/docs/openapi-spec/tokens/tokens.yaml` return 404. This is fine for humans clicking links, but agents benefit from a stable catalog page of canonical spec URLs.
- Fetching `/docs/price/v3` as Markdown redirects to `/docs/price.md`. The resulting page is useful, but the redirect is mildly surprising because the API reference itself is versioned as Price V3.
- Keyless access is useful, but the rate limit requires local throttling. A tiny "keyless mode" example that intentionally sleeps between calls would help agents avoid accidental 429s.
- Tokens search includes `usdPrice` and Price API also returns price data. The docs explain Price API as the price source of truth, but a short "when Tokens price is enough versus when to call Price V3" note would reduce ambiguity.
- Token audit fields are valuable but not fully explained on the main Tokens overview page. A field-level example for common warning flags would help UI builders present trust signals without overclaiming.
- Python's default `urllib` request signature was blocked by Cloudflare 1010 even though the same endpoint worked through `curl`. Adding a descriptive `User-Agent` fixed this, but an agent-focused troubleshooting note would save time.
- The CLI docs are clear that the package is pre-v1 and JSON-friendly, but safe read-only examples are not prominent. An explicit `jup --version`, config inspection, or market-data-only command would let agents validate CLI setup before any wallet/key/trading workflow.

## API Details Exercised

- `GET https://api.jup.ag/tokens/v2/search?query=JUP`
- `GET https://api.jup.ag/price/v3?ids=<mint1>,<mint2>`
- `GET https://developers.jup.ag/docs/llms.txt`
- `GET https://developers.jup.ag/docs/skill.md`
- `GET https://developers.jup.ag/docs/openapi-spec/tokens/v2/tokens.yaml`
- `GET https://developers.jup.ag/docs/openapi-spec/price/v3/price.yaml`

## Suggested Platform Improvements

- Put the agent-first quickstart in one visible path: docs index, keyless call, API key setup, and one complete read-only sample.
- Add a recommended local environment variable convention such as `JUP_API_KEY` to every language example.
- Add a machine-readable endpoint catalog link beside each API overview page, not only in the broader docs index.
- Add explicit guidance for safe read-only prototyping versus transaction-building endpoints.
- Expand `skill.md` from a repository pointer into a compact navigator that includes skill names and install commands.
- Add one no-wallet CLI verification path for agents before showing swap/lend/perps examples.

## Submission Readiness

To finish the bounty submission cleanly, the remaining operator-gated item is a Jupiter Developer Platform account/API key and the account email required by the listing. The project itself runs in keyless mode and is ready to publish/update as a public GitHub repo.
