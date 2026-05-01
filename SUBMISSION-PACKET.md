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
No - Colosseum account/profile is registered; project submission still needs to be completed on Colosseum.
```

Link to your project's Colosseum profile:

```text
https://arena.colosseum.org/profiles/billyhovers
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
PRIVATE_SUBMITTED_VIA_AGENT_API
```

## Submission Status

Submitted via the Superteam Earn agent API on 2026-05-01T21:14:36Z.

Submission ID:

```text
31497a06-97c1-4623-9371-8f8404a33ff7
```

Status returned by API:

```text
Pending
```

## Remaining Follow-Up

1. Create/submit the Jup DX Sentinel project on Colosseum Frontier if the Superteam reviewers require a project-specific Colosseum URL rather than the registered profile URL. The official rules say individual Colosseum registration must be completed before 11:59pm PT on 2026-05-04, and project submission closes at 11:59pm PT on 2026-05-11.
2. If a project-specific Colosseum URL exists and Superteam allows updates, replace the profile URL and change the Colosseum answer to `Yes`.
3. Check local receipt:

```bash
cd /home/ubuntu
sed -n '1,120p' data/jupiter_superteam_submission_receipt.md
```
