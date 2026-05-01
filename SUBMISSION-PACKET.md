# Superteam Submission Packet

Listing: https://superteam.fun/earn/listing/not-your-regular-bounty  
Project: Jup DX Sentinel  
Prepared: 2026-05-01

## Current Status

The project and DX report are public and runnable. The Superteam agent API credentials are valid, and the submission endpoint accepts authenticated requests at:

```text
POST https://superteam.fun/api/agents/submissions/create
```

The endpoint currently validates these top-level fields:

- `listingId`
- `link`
- `eligibilityAnswers`

## Required Submission Answers

Project Title:

```text
Jup DX Sentinel
```

Project Description:

```text
Read-only Jupiter Developer Platform experiment that combines Tokens API search, Price API V3, and an AI/docs stack probe into a token-quality snapshot plus a concrete DX report. It tests keyless prototyping, API-key production expectations, llms.txt, skill.md, Markdown docs export, OpenAPI specs, and safe CLI discovery without wallet signatures or transaction-writing calls.
```

Project GitHub Link:

```text
https://github.com/ramimbo/jup-dx-sentinel
```

Feedback doc/markdown file:

```text
https://github.com/ramimbo/jup-dx-sentinel/blob/master/DX-REPORT.md
```

Project Website:

```text
https://github.com/ramimbo/jup-dx-sentinel
```

Did you submit this project to the official Frontier Hackathon on Colosseum? (Yes/No):

```text
REQUIRED_OPERATOR_GATE
```

Link to your project's Colosseum profile:

```text
REQUIRED_OPERATOR_GATE
```

Link to your Loom / Demo Video:

```text
optional
```

Presentation Link:

```text
optional
```

Developer Platform account email:

```text
REQUIRED_OPERATOR_GATE
```

## Remaining Gates

1. Sign in to https://developers.jup.ag/portal, create or confirm the Jupiter Developer Platform account, and provide the account email.
2. Create or confirm the Colosseum Frontier project profile required by the Superteam form. The official rules say individual Colosseum registration must be completed before 11:59pm PT on 2026-05-04, and project submission closes at 11:59pm PT on 2026-05-11.
3. Replace the `REQUIRED_OPERATOR_GATE` placeholders in `superteam-submission.draft.json`.
4. Submit with:

```bash
cd /home/ubuntu
scripts/superteam_agent_cli.py submit jup_dx_sentinel/superteam-submission.draft.json --yes
```

Dry run:

```bash
cd /home/ubuntu
scripts/superteam_agent_cli.py submit jup_dx_sentinel/superteam-submission.draft.json --dry-run
```
