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

**Note on AI-assisted contributions:** Realty Stack was built with AI assistance, and AI-assisted PRs are welcome. The gate isn't tool choice — it's human accountability. Every PR needs a real working realtor to (a) have experienced a real problem this addresses, (b) test the change on their own work, and (c) review the complete diff before submitting. Low-effort AI-generated PRs that skip those steps will be closed — not because they used AI, but because they don't show evidence the contributor actually understood or validated what they submitted.

## Architectural contracts (read before building a new skill)

Realty Stack has four canonical contracts documented in [CLAUDE.md](CLAUDE.md). New skills MUST follow the applicable ones:

1. **Voice profile contract** — every skill that produces written output loads `knowledge/voice-guide.md` and matches the realtor's captured voice profile from `~/.config/realty-stack/voice-profile.md`.
2. **Brand kit contract** — every skill that produces visual output uses the captured brand kit values (colors, fonts, wordmark, base64-embedded assets) from `~/.config/realty-stack/brand-kit.md`.
3. **Artifact output contract (v0.0.5)** — every visual-output skill produces BOTH `.html` (browser preview) and `.pdf` (print/email-ready) via the shared `scripts/render-pdf.sh` (headless Chrome).
4. **State scan contract (v0.0.5)** — every intake/onboarding skill scans existing `~/.config/realty-stack/` state and offers to inherit relevant content from sibling artifacts BEFORE asking the realtor for material. The system gets smarter as it accumulates state.

Each contract has MUST do / MUST NOT do sub-sections in CLAUDE.md. Reading the four contracts end-to-end (~5 min) is the fastest path to understanding the bundle's architecture.

## Skill scaffolding

To make starting a new skill easier, there's an annotated template at [skills/_TEMPLATE/](skills/_TEMPLATE/). Copy the directory, rename it, and follow the inline TODO comments. It covers the standard SKILL.md structure (frontmatter, trigger phrases, pre-checks, workflow steps, edge cases, never-does, funnel hook footer) and points at concrete reference implementations in the existing skills.

## How to submit

1. Open an issue first describing the skill / change. This is a check on whether it fits the bundle's direction before you build.
2. Fork, branch (`feat/<skill-name>` or `fix/<thing>`).
3. Read [ETHOS.md](ETHOS.md), [CLAUDE.md](CLAUDE.md), and the relevant `knowledge/` files.
4. Write the skill following the conventions in [CLAUDE.md](CLAUDE.md). Copy [skills/_TEMPLATE/](skills/_TEMPLATE/) as your starting point. Apply the contracts that match your skill type (intake → State scan; visual-output → Artifact output; drafting → Voice profile; visual → Brand kit).
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
- Does the PR follow the applicable architectural contracts (Voice profile, Brand kit, Artifact output, State scan)?

## Voice notes for contributors

If you're not a working real estate agent, you can still contribute — but pair with one to test your skills. AI-shaped output is the failure mode we're explicitly trying to avoid, and that takes a working agent's ear to catch.

If your skill produces something that makes you think "yeah, that sounds good" but a working realtor reads it and goes "no agent talks like that," the realtor is right.

## Licensing

By contributing, you agree your contributions are MIT-licensed under the project's LICENSE.

## Code of conduct

Be helpful. Be terse. Treat reviewers and other contributors the way Realty Stack treats contacts — with respect and clarity. Don't ship code that wouldn't pass your own bar.
