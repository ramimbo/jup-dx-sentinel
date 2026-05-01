# Jupiter AI Stack Probe

Generated: 2026-05-01T21:03:00+00:00
Token query: `JUP`

## Surface Checks

| Surface | Status | Final URL | Content Type |
| --- | ---: | --- | --- |
| `llms.txt` | 200 in 699ms | https://developers.jup.ag/docs/llms.txt | `text/plain; charset=utf-8` |
| `skill.md` | 200 in 70ms | https://developers.jup.ag/docs/skill.md | `text/markdown; charset=utf-8` |
| `ai-overview-md` | 200 in 146ms | https://developers.jup.ag/docs/ai.md | `text/markdown; charset=utf-8` |
| `tokens-md` | 200 in 482ms | https://developers.jup.ag/docs/tokens/token-information.md | `text/markdown; charset=utf-8` |
| `price-md` | 200 in 236ms | https://developers.jup.ag/docs/price.md | `text/markdown; charset=utf-8` |
| `tokens-openapi` | 200 in 74ms | https://developers.jup.ag/docs/openapi-spec/tokens/v2/tokens.yaml | `application/octet-stream, text/yaml` |
| `price-openapi` | 200 in 71ms | https://developers.jup.ag/docs/openapi-spec/price/v3/price.yaml | `application/octet-stream, text/yaml` |

## Parsed Signals

- `llms.txt` linked documentation pages found: 227
- `llms.txt` mentions keyless access: yes
- `llms.txt` mentions CLI: yes
- `llms.txt` mentions MCP: yes
- `llms.txt` mentions skills: yes
- `skill.md` non-empty line count: 3
- Markdown docs fetched successfully: ai-overview-md, tokens-md, price-md
- OpenAPI specs fetched successfully: tokens-openapi, price-openapi

## Read-Only API Smoke

- Tokens search status: 200 in 93ms; returned 20 rows.
- Price V3 status: 200 in 76ms; returned 5 priced mints.

## CLI Registry Check

- `@jup-ag/cli` latest version: `0.10.0`
- Description: CLI for interacting with Jupiter's products on Solana: Spot, Perps, Lend, Prediction Markets, Token Verification and more.

## DX Notes

- The AI docs are genuinely useful as a starting map: `llms.txt` exposes keyless limits, portal setup, API families, and AI tooling in one file.
- `skill.md` is reachable, but it is only a high-level pointer to the agent-skills repository. An inline list of available skill names and install commands would save an agent one extra hop.
- The OpenAPI specs are easy to discover from `llms.txt`, but guessed shorter paths such as `/docs/openapi-spec/price/price.yaml` return 404. Agents should follow the exact spec links.
- The docs export path works well with `.md` pages and `Accept: text/markdown`; `/docs/price/v3` redirects to the broader price markdown page, which is harmless but slightly surprising.
- The npm package metadata is visible without installation, which is enough for safe agent discovery before any key, wallet, or trading command is configured.
- This probe intentionally does not install the CLI, configure keys, connect a wallet, place orders, or call transaction-writing endpoints.
