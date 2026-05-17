# voice-draft v2 — Design Spec

**Status:** Approved 2026-05-16. Ready for implementation plan.
**Author:** Holden Richardson
**Skill:** `skills/voice-draft/`
**Supersedes:** the v0.0.1 voice-draft design (per-invocation sample-paste pattern)

---

## TL;DR

`voice-draft` is the **one-time onboarding skill** every Realty Stack user runs on install. It captures the agent's writing voice in two distinct modes (email + text), plus basic profile info (name, brokerage, market, signoff), and persists the result to a local file. From that point forward, every other Realty Stack skill that produces written output reads the voice profile via the `using-realty-stack` overlay and drafts in the agent's voice without re-asking for samples.

This is the foundation that makes the rest of the bundle feel like *the agent's* AI rather than a generic LLM.

---

## Motivation

The v0.0.1 design asked the realtor to paste 3+ message samples + intent every single time they invoked voice-draft. That's:

- Friction-heavy per-invocation
- Forces other skills (follow-up-draft, listing-description, etc.) to either replicate the same paste-samples pattern or accept generic LLM-voice output
- Doesn't accumulate value — every session starts from zero

v2 inverts this: pay the onboarding cost **once** (~5 min), get voice-matched output across every Realty Stack skill **forever** (on this device).

---

## Scope

### In scope
- The voice-draft skill's onboarding workflow (capture → analyze → confirm → refine → persist)
- The voice profile file format on disk
- The SessionStart hook that auto-triggers voice-draft for first-time users
- The first-skill-invocation fallback trigger
- The integration contract: how the `using-realty-stack` overlay loads the profile and how downstream skills consume it
- Edge-case handling (thin samples, template-only samples, interrupted onboarding, corrupted profile file)

### Out of scope (v0.0.1)
- Multi-device sync (per-device only; Realty Brain is the future paid sync path)
- Voice profile refresh / re-capture skill (`/realty-stack:refresh-voice` — defer to v0.0.2; for now, manually delete the file)
- Auto-learning from sent messages over time (that's a Realty Brain feature)
- Multiple voice profiles per agent (e.g., "formal seller voice" vs "casual buyer voice" — the email/text split handles the dominant case)
- Voice profile sharing across team members (brokerage-wide voice library — Realty Brain Team feature)

---

## Design

### UX flow

1. **Install.** Realtor runs `claude plugins install github.com/holdengr/realty-stack`. Plugin installs silently.

2. **First session post-install.** Realtor opens a Cowork project or Claude Code session. The plugin's SessionStart hook fires, checks for `~/.config/realty-stack/voice-profile.md`, finds it missing, and injects an opening prompt:

   > *"Realty Stack is loaded. Before you use any skills, let's capture your writing voice — takes about 5 minutes, one-time. Want to do it now?"*

3. **Onboarding starts.** When the realtor says yes (or asks any natural-language equivalent), the voice-draft skill activates and walks through:

   **Step A — Basic profile (4 fields):**
   - Full name (as it should appear in signatures)
   - Brokerage
   - Primary market (city/region — anchors the "Practical & Local" voice tenet)
   - Preferred signoff for email AND for text (optional — inferred from samples if not provided)

   **Step B — Email samples:** "Paste 3-5 substantial emails you've actually sent in a real estate context. Substantial means more than a one-liner — at least a few sentences each. Diverse helps (one to a lead, one to a client under contract, one to another agent, etc., but not required)."

   **Step C — Text samples:** "Same thing for texts — 3-5 substantial real estate texts you've actually sent. Doesn't have to be long; just real."

4. **Analysis.** System reads both batches, builds an email-voice profile and a text-voice profile (described below).

5. **Confirmation.** System returns three things in one response:
   - **Voice summary** — short plain-English description of what was captured (~150-300 words per voice)
   - **Example email** — drafted on a generic real-estate scenario (default: "follow up with a hot buyer lead about a new listing")
   - **Example text** — drafted on a generic scenario (default: "let a past client know about a listing that just dropped in their old neighborhood")

6. **Approval or refinement.**
   - Realtor says "yes, that's me" (or anything semantically equivalent) → voice profile written to disk; onboarding complete.
   - Realtor gives freeform feedback (any complaint or correction, in plain English) → system adjusts the voice profile per the feedback, regenerates the examples, asks again. Loop until approval.

7. **Done.** Voice profile is live. Every subsequent Realty Stack skill the realtor invokes uses it automatically.

### Fallback trigger (belt + suspenders)

If the realtor somehow bypasses the SessionStart prompt (dismissed it, uses Cowork programmatically, opens a session that doesn't fire the hook, etc.), the first time they invoke ANY Realty Stack skill that produces written output, that skill detects missing voice profile and runs voice-draft inline before continuing with their request.

Example: realtor's first real action is *"draft a follow-up to Sarah."* The `follow-up-draft` skill loads, sees no voice profile, runs voice-draft onboarding to completion, then returns to the original "draft a follow-up to Sarah" task.

### Voice profile file

**Location:** `~/.config/realty-stack/voice-profile.md` (single Markdown file, per-device, no sync)

**Format example:**

```markdown
# Realty Stack — Voice Profile for Holden Richardson
Captured: 2026-05-16
Refined: 2026-05-16 (2 rounds)

## Agent Profile
- Name: Holden Richardson
- Brokerage: 616 Realty
- Market: Grand Rapids, MI
- Email signoff: "— Holden" (casual) / "Holden Richardson | 616 Realty" (formal)
- Text signoff: "— H" or none

## Email Voice

[150-300 word plain-English description of how this agent writes emails.
Tone, register, openness, sentence rhythm, what they do that's distinctive,
what they don't do that AI tends to do. Written so a downstream skill can
read it and "play the role" of this agent at a keyboard.]

### Observed patterns
- Sentence length: ~12 words average, range 5-30
- Common openers: "Hey [name],", "[Name] —", "Quick one —"
- Common signoffs: "— Holden", occasional "Holden Richardson | 616 Realty" for formal threads
- Em-dash usage: heavy
- Hedge word frequency: low ("just" rare, "actually" rare, "I think" rare)
- Exclamation points: very rare
- Emoji: never
- Notable phrasings: prefers neighborhood names ("Heritage Hill") over generic ("downtown"); uses "we" for buyer-agent collaboration

## Text Voice

[150-300 word plain-English description, same shape as Email Voice above
but for texts. Usually noticeably more clipped, fragments encouraged,
less formal.]

### Observed patterns
- Sentence length: ~6 words average
- Fragment use: heavy
- Common openers: first-name only ("Sarah —"), sometimes nothing
- Common signoffs: "— H" or none
- Em-dash usage: heavy
- Emoji: only mirrors contact's usage
- Notable phrasings: skips greetings on quick replies; uses lowercase often

## Source Samples (preserved for future re-analysis)

### Emails
[3-5 raw email samples, separated by `---`]

### Texts
[3-5 raw text samples, separated by `---`]

## Refinement History
- Round 1 (2026-05-16): captured from 4 emails + 5 texts + profile (Holden Richardson, 616 Realty, Grand Rapids MI, signoffs inferred)
- Round 2 (2026-05-16): agent flagged "emails too stiff on opener" → relaxed default opener from "Hi [name]," to "Hey [name],"
```

**Why Markdown:**
- LLM-friendly to load and reason about (no JSON parsing step)
- Human-readable so the realtor can inspect and hand-edit if they want
- Easy to version and diff
- Structured enough that downstream skills can grep specific sections (e.g., just the signoff lines) if they need to

### Consumption by other skills

The `using-realty-stack` overlay reads `~/.config/realty-stack/voice-profile.md` at session start and injects its contents into context. Every Realty Stack skill that loads in the overlay's session has the voice profile available — no per-skill load code, no risk of forgetting.

**Token cost:** ~800-1500 tokens always-on per session (a typical voice profile). Acceptable given the value across every drafting skill in the bundle.

**Contract for skill authors:** when writing a new Realty Stack skill that produces agent-voice output, assume the voice profile is in context. Match the email voice when drafting emails, the text voice when drafting texts, the agent profile fields (name, brokerage, market) for any contextual specifics. Don't ask the realtor for samples — they already onboarded.

### Edge cases & failure modes

| Situation | Behavior |
|---|---|
| Realtor provides fewer than 2 samples in either email or text batch | Skill pushes back: *"I need at least 2 real samples per category to capture your voice. Got a couple more?"* Doesn't attempt to analyze on insufficient data. |
| Samples are all CRM-template-looking (boilerplate, identical structure) | Skill flags in confirmation: *"These look like template responses. Captured what I can, but voice quality will be better with more conversational samples — texts to a friend-of-friend lead, follow-ups after a showing, that kind of thing. Want to add a few?"* |
| Samples are wildly inconsistent (clearly multiple voices) | Skill notes in confirmation: *"Your samples look like they're from a few different drafters. Captured what I think is most consistently yours — let me know if the result feels off."* |
| Onboarding interrupted halfway (realtor closes the session, kills the process) | Voice profile file is NOT written until refinement is approved. On next session, SessionStart re-prompts and starts fresh. No partial state to manage. |
| Voice profile file exists but is corrupted / unparseable | Overlay detects on load (parse failure), re-triggers onboarding with: *"Looks like your voice profile got corrupted — let's redo it."* |
| Realtor wants to redo voice later (changed brokerages, voice evolved) | Out of scope for v0.0.1. Workaround: realtor manually deletes `~/.config/realty-stack/voice-profile.md` and triggers onboarding again. Add a `/realty-stack:refresh-voice` skill in v0.0.2. |
| Realtor uses Realty Stack across two devices (Holden's case) | Each device captures its own voice profile (per-device, no sync). Onboarding repeats on the second device. Documented as a known limitation; Realty Brain is the future sync path. |
| Realtor is mid-onboarding and asks an unrelated question | Skill should gracefully pause and answer the question, then offer to resume onboarding. Don't lose state. |

### Things this design explicitly does NOT do

- **Auto-learn voice over time.** The profile is captured once at onboarding. Updates require explicit re-onboarding (manual file delete + re-trigger). Continuous learning is a Realty Brain feature.
- **Sync across devices.** Per-device only. Documented; Realty Brain is the upgrade path.
- **Capture more than two voice modes.** Email and text only. Different voices for different contacts/scenarios (e.g., "formal seller voice" vs "casual buyer voice") are out of scope for v0.0.1.
- **Share voice profiles across team.** Each realtor's profile is their own. Brokerage-wide voice libraries are a Realty Brain Team feature.

---

## Implementation surface (what changes in the repo)

### New
- `hooks/hooks.json` — SessionStart hook that runs a small script to check for `~/.config/realty-stack/voice-profile.md` and inject a prompt if missing
- `hooks/scripts/check-voice-profile.sh` — the actual check script (one-liner that outputs the prompt to stdout when profile is missing)
- `docs/specs/2026-05-16-voice-draft-v2-design.md` — this document

### Rewritten
- `skills/voice-draft/SKILL.md` — full rewrite per this design (replaces the per-invocation sample-paste pattern with the one-time onboarding workflow)
- `skills/using-realty-stack/SKILL.md` — add step at session start: read `~/.config/realty-stack/voice-profile.md` if it exists, inject into context; if missing, defer to SessionStart hook's prompt
- `CLAUDE.md` — document the voice profile file location, format, and the contract that every drafting skill should expect it in context

### Unchanged
- `knowledge/voice-guide.md`, `knowledge/constitution.md`, `knowledge/fair-housing.md` — these stay as global rules that govern all output regardless of voice profile
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — no changes
- All other repo docs (README, ETHOS, CONTRIBUTING, SECURITY, LICENSE, CHANGELOG, VERSION)

---

## Open questions for the implementation plan

None blocking. Specific implementation choices to nail down in the writing-plans pass:

1. **Exact wording of the SessionStart prompt.** Draft included above but tone it for first-time-user friendliness.
2. **Exact wording of the freeform-feedback prompt.** Specifically: how does the skill nudge the realtor to be specific rather than vague? ("Tell me what's off — be as specific or as gut-feel as you want, both work.")
3. **The generic example scenarios for confirmation.** Pick 2 default scenarios (one for email, one for text) that exercise voice meaningfully without being so specific they prejudice the realtor's reaction.
4. **Hook script implementation.** Bash one-liner or short Python — whatever's portable across Mac + Linux Cowork containers.

---

## Success criteria

This design is working when:

1. A new realtor can install the plugin and have a functional voice profile within 10 minutes (5 min onboarding + 5 min for any refinement rounds).
2. After onboarding, a follow-up-draft skill (when it exists) produces a draft that the realtor sends with no edits at least 70% of the time.
3. The realtor never has to paste their voice samples again in subsequent sessions.
4. The voice profile file is small enough (~1500 tokens max) that always-on session injection doesn't bloat context noticeably.
5. Edge cases (thin samples, interrupted onboarding, corrupted file) all degrade gracefully — no silent failures, no half-written profiles, no awkward UX.

---

## Next step

Invoke the `writing-plans` skill to produce the implementation plan from this design.
