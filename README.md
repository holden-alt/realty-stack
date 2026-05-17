# Realty Stack

**AI skills for residential real estate agents who actually close deals.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Version](https://img.shields.io/badge/version-0.0.2-orange.svg)](VERSION) [![Claude](https://img.shields.io/badge/built%20for-Claude-purple.svg)](https://claude.ai)

Open-source. MIT. Free. Built by a working realtor who codes — for working realtors who want their AI to sound like *them*, not like a marketing intern.

---

## Why this exists

There are two kinds of AI tools for real estate right now:

1. CRM bolt-ons from companies that have never closed a deal — generic, expensive, push their own ecosystem
2. Open-source skill bundles from developers who have never closed a deal — interesting toys, not daily-use tools

Realty Stack is the third kind. Built by **Holden Richardson** — Grand Rapids realtor + AI engineer running 1,500+ FUB contacts and 30+ closed deals through the actual workflows these skills target. Tested on real work before every commit.

The bar: every output sounds like you wrote it, respects your contacts, and stays inside fair housing / NAR / state compliance lines. If it doesn't, the skill is wrong — we fix it.

---

## 30-second install (Claude Code + Cowork)

```bash
claude plugins install github.com/holdengr/realty-stack
```

Then in any Claude Code or Cowork session, ask Claude to "load realty stack" (or "using realty stack") and the session-start overlay loads — brand voice tenets, the constitution, and fair-housing guardrails go into context.

After that, just describe what you need: *"draft a text to Sarah about the new Madison Ave listing"* — Claude routes to the right skill (`voice-draft` in this case) automatically. No slash-typing required.

**Other surfaces** (Claude.ai chat, Codex, Cursor, Gemini) are not supported in v0.0.2. We'll add them based on demand from real users.

---

## See it work

Real onboarding sequence from a fresh install:

**Install:** `claude plugins install github.com/holdengr/realty-stack` — done.

**First Cowork session after install:** Realty Stack auto-prompts:

> *"Realty Stack is loaded. Before you use any skills, let's capture your writing voice — takes about 5 minutes, one-time. Want to do it now?"*

**Holden:** "yes"

→ Voice-draft walks through: name, brokerage, market, signoffs (4 quick fields), then 3-5 real emails Holden pastes, then 3-5 real texts. Analysis runs (~30 seconds). Returns:

> *Email voice: short, direct. Em-dashes for clauses. Opens with "Hey [name]," or "[Name] —". Signs "— Holden" casually, "Holden Richardson | 616 Realty" formally. No exclamation points unless an offer actually got accepted...*
>
> *Text voice: very clipped — fragments encouraged. Opens with first name only or nothing. Signs "— H" or none. Em-dashes everywhere. Never emoji unless the contact uses them first...*
>
> *Example email (follow-up to hot buyer about new comparable):* [drafted email in Holden's voice]
>
> *Example text (past-client neighborhood listing alert):* [drafted text in Holden's voice]
>
> *"Sound like you? Or refine?"*

**Holden:** "yes that's me" → onboarding complete, voice profile written to `~/.config/realty-stack/voice-profile.md`. **Total time: ~5 minutes.**

**From this point forward**, every Realty Stack skill (follow-up-draft, listing-description, meeting-distill, etc.) produces output in Holden's voice automatically. He never pastes voice samples again.

---

## Skills (v0.0.2)

Skills auto-route based on what you ask Claude. You don't type slashes — you describe what you need.

| Skill | Triggers on | What it does |
|---|---|---|
| `voice-draft` (one-time, on install) | Auto-fires on first session post-install; also "set up my voice", "onboard me", "configure realty stack" | Captures the realtor's email + text voice + basic profile. Persists to `~/.config/realty-stack/voice-profile.md`. Future drafting skills auto-use it. ~5 min one-time setup. |

More skills land daily — see [CHANGELOG.md](CHANGELOG.md) for the rolling release log.

**Coming this week (Tier 1 — universal, no FUB required):**

| Skill | Triggers on | What it does |
|---|---|---|
| `follow-up-draft` | "follow up with...", "reach out to...", "touch base with..." | Specific-contact follow-ups in your voice with adaptive cadence reasoning. |
| `meeting-distill` | "distill this meeting", "summarize this transcript", "extract action items from..." | Granola transcript → action items + key takeaways + drafted follow-up + drafted FUB note. |
| `listing-description` | "write a listing for...", "MLS copy for...", "describe this property..." | Property details → MLS-ready listing copy. Fair-housing checked. |
| `cma` | "run a CMA on...", "comparative market analysis", "comp this property..." | Subject + 3-5 comps → CMA narrative + price recommendation + rationale. |

**Coming Weeks 3-4 (Tier 2 — connects to your FUB account via the bundled `fub-mcp-server`):**

`connect-fub` wizard, `fub-audit`, `action-plan-builder`, `revival-campaign-launcher`, `past-client-tagger`, and ~10 more.

The full 33-skill roadmap is in the project plan; tracking via GitHub issues.

---

## What makes this different

- **Voice-opinionated.** Every skill loads `knowledge/voice-guide.md` and self-checks against 6 brand voice tenets before returning output. Not generic. Direct, calm, practical, slightly blunt, mature.
- **Compliance baked in.** Fair housing language guardrails are loaded as a knowledge file, not a vibes-based check. Listings, follow-ups, marketing — all checked before they reach you.
- **No CRM lock-in.** Tier 2 uses FUB because FUB is what the alpha cohort uses, not because of commercial coupling. The bundled `fub-mcp-server` is MIT, auditable, forkable. Other CRM adapters land based on user demand.
- **No telemetry.** Skills don't phone home. Your FUB key lives only on your machine (or your Cowork project secrets). We never see your data.
- **Tested on real deals.** Holden uses every skill on his actual work before he commits it.

---

## The paid sibling — Realty Brain

Realty Stack is pull-based: you invoke skills when you want them.

**[Realty Brain](https://realtybrain.com)** is push-based: it watches your FUB + email + calendar continuously, drafts proactively, learns your voice over time, and sends a morning brief to your Slack with the day's highest-leverage moves.

- $99/mo
- All Realty Stack skills + 10 Tier-3 always-on skills only available in Brain
- Continuous voice training from your sent messages
- Realty Stack is the wedge. Realty Brain is the upgrade.

You don't need it. Realty Stack stands on its own.

---

## Ethos

Realty Stack is governed by [ETHOS.md](ETHOS.md):

- Truth over reassurance
- Honor the contact-realtor relationship
- Show before do (every change previews; you approve)
- No personification (skills never sign their own name to your contacts)
- Adaptive cadence (context overrides timer)
- Material change only (no spam)
- The realtor is the executor

Read it before contributing.

---

## Contribute

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) — every new skill needs (a) brand voice fit, (b) compliance citation if relevant, (c) a real-scenario test case in the PR description.

Issues for: bug reports, skill requests, fair housing language flags we missed.

Security disclosures: see [SECURITY.md](SECURITY.md).

---

## Acknowledgments

Built on top of the [Agent Skills standard](https://docs.claude.com/en/docs/agents-and-tools/agent-skills). Inspired by what generic AI tools for real estate failed to deliver. Special nod to the [superpowers](https://github.com/obra/superpowers) plugin for proving disciplined skill stacks beat ad-hoc prompts.

---

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Holden Richardson.
