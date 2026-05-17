# Contributing to Realty Stack

Realty Stack is opinionated by design. Contributions are welcome — but they need to clear the bar.

## What we're looking for

- **New skills** that fit the Tier 1 / Tier 2 / Tier 3 architecture (see [CLAUDE.md](CLAUDE.md))
- **Compliance improvements** — flagged phrases we missed, state-specific disclosure rules, accessibility language
- **Voice refinements** — examples where a skill produced AI-shaped output instead of realtor-shaped output
- **Multi-harness adapters** — Codex / Cursor / Gemini wrappers

## What we're NOT looking for

- CRM lock-in beyond FUB (Tier 2 is FUB because the alpha cohort uses FUB; if you want to add another CRM, open an issue first to discuss the integration path)
- Telemetry / analytics / "phone home" features
- Marketing-heavy or hype-shaped skill outputs
- Skills that auto-send, auto-deploy, or otherwise bypass T18 ("show before do")
- "Generic LLM tricks dressed in real-estate clothing" — every skill earns its place by solving a real, frequent realtor workflow

## How to submit

1. Open an issue first describing the skill / change. This is a check on whether it fits the bundle's direction before you build.
2. Fork, branch (`feat/<skill-name>` or `fix/<thing>`).
3. Read [ETHOS.md](ETHOS.md), [CLAUDE.md](CLAUDE.md), and the relevant `knowledge/` files.
4. Write the skill following the conventions in [CLAUDE.md](CLAUDE.md).
5. Test it on a real scenario from your own work.
6. Open the PR with:
   - Sanitized input/output from your real-scenario test
   - One-sentence quality note
   - Fair-housing check pass/flag if the skill produces contact-facing copy
   - Reference to the issue that scoped this

## What the maintainer will check

- Does the output sound like a real, experienced realtor?
- Does the skill respect every relevant constitutional tenet (T1, T5, T8, T14, T15, T16, T18)?
- Are compliance references cited inline?
- Is the skill scoped tight (does one thing well, not seventeen things mediocre)?
- Does it work without breaking on edge cases (missing inputs, weird contact context, malformed transcripts)?

## Voice notes for contributors

If you're not a working real estate agent, you can still contribute — but pair with one to test your skills. AI-shaped output is the failure mode we're explicitly trying to avoid, and that takes a working agent's ear to catch.

If your skill produces something that makes you think "yeah, that sounds good" but a working realtor reads it and goes "no agent talks like that," the realtor is right.

## Licensing

By contributing, you agree your contributions are MIT-licensed under the project's LICENSE.

## Code of conduct

Be helpful. Be terse. Treat reviewers and other contributors the way Realty Stack treats contacts — with respect and clarity. Don't ship code that wouldn't pass your own bar.
