---
name: listing-presentation-template
description: This skill should be used when a real estate agent asks to "set up my listing presentation", "build my listing pitch", "create my listing presentation template", "I want a listing presentation", "configure my listing template", or "build my listing presentation template". One-time consultative builder that captures the agent's reusable listing-presentation content (about-me, process, marketing philosophy, track record, testimonials, pricing, fees) and persists to ~/.config/realty-stack/listing-presentation-template.md so per-listing /listing-presentation can render in seconds.
version: 0.0.1
---

# Listing Presentation Template — Build Once, Fill Per Appointment

One-time consultative onboarding that captures the agent's reusable pitch content. Paid once in time; every listing appointment after benefits. Sibling to `/cma` — this skill is about the AGENT (process, philosophy, track record); `/cma` is per-property analytics. Mirrors voice-draft + brand-kit-capture's one-time-onboarding-then-persist architecture.

---

## When this skill runs

Trigger phrases:

- "set up my listing presentation"
- "build my listing pitch"
- "create my listing presentation template"
- "I want a listing presentation"
- "configure my listing template"
- "build my listing presentation template"

**Inline fallback:** `/listing-presentation` runs this skill inline if `~/.config/realty-stack/listing-presentation-template.md` is missing, then returns to the per-listing request.

---

## Voice profile + brand kit pre-checks

Before any template work, verify both pre-requisites:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion. Template prose is drafted in Email Voice (long-form professional doc).
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion. Headshot may come from brand kit assets; brand voice notes inform tone.

Pattern matches `/cma`. Never produce un-voiced or un-branded output.

---

## Onboarding workflow

Work through Steps A through H in order. Do not write the template file until Step H.

### Step A — Front-loaded data dump

Ask once, in a single message:

> *"To build your listing presentation, I need everything you already have about your business. Drop anything that's relevant — paste, attach, or describe:*
>
> *- Old listing presentations (PDF or text)*
> *- Your bio (website 'About' page, brokerage profile)*
> *- Testimonials (with or without client names — your call)*
> *- Sample listings you'd showcase (addresses, prices, days on market)*
> *- Your brokerage's marketing assets (if any)*
> *- Headshot / professional photo (if not already in brand kit)*
> *- Any awards, certifications, sales stats, or recognition*
> *- Stories about your process — what you actually do for sellers*
>
> *Don't worry about organizing it. I'll sort it. If you're starting fresh and have nothing, that's fine too — I'll ask targeted questions instead."*

Realtor pastes / drops / describes. Read PDFs via the Read tool's `pages` parameter where applicable. Empty dump is valid — Step B detects and skips straight to Step D with all sections as gaps.

### Step B — Analyze the dump

Categorize dump content into the 8 standard sections:

1. **About Me** — bio, credentials, years in business, personal differentiators
2. **Why Hire Me** — value prop, what the seller gets from working with this agent
3. **My Selling Process** — phases, milestones, what happens between listing and closing
4. **Marketing Philosophy** — channels, approach to reaching buyers (NOT property-specific tactics)
5. **Recent Track Record** — recent listings, sale prices, days on market, list-to-sale ratios
6. **Testimonials** — client quotes (with or without names / photos)
7. **Pricing Philosophy** — general approach to pricing strategy (NOT a specific CMA)
8. **Fee Structure** — commission, what's included, what isn't, who pays what at closing

Also identify recurring themes that suggest additional custom sections (e.g., "your dump mentions community involvement 5 times — want a Community / Local Specialization section?").

### Step C — Propose the structure

Return a single confirmation message:

- Covered sections (with source material)
- Gaps (sections with no source material in the dump)
- Suggested additional sections (themes from the dump that don't fit the standard 8)
- Proposed final section list with order

Ask: *"Here's the structure I'd propose. Add / remove / reorder anything. For the gaps, I'll ask targeted questions to fill them in next."*

### Step D — Confirm sections + fill gaps

Realtor confirms the section list (any edits). Ask targeted questions for sections with no source material only. Section-specific questions:

- **About Me:** years licensed, brokerage, what's distinctive about your background
- **Why Hire Me:** what's different about working with you vs the agent down the street
- **My Selling Process:** walk me through what happens between "we sign the listing agreement" and "we close"
- **Marketing Philosophy:** how do you actually reach buyers — channels you use, channels you avoid
- **Recent Track Record:** past listings (addresses or partial — agent's call), prices, DOM, any standout outcomes
- **Testimonials:** paste 3-5 client quotes; note for each whether to include client name (and whether to include a photo path)
- **Pricing Philosophy:** how do you think about pricing strategy in general — aggressive, conservative, market-driven, hybrid
- **Fee Structure:** your commission %, what's included in the fee, what closing costs go to whom

Skip any section the dump covered thoroughly.

### Step E — Draft each section in Email Voice

For each section, draft prose using the realtor's Email Voice from their voice profile:

- Match sentence length patterns, opener style, signoff usage
- Use "Practical & Local" — name specific streets, neighborhoods, brokerage details, not generic descriptors

**COMPLIANCE DISCIPLINE:**

- No fair housing red flags ("such a nice family", neighborhood demographic descriptors)
- No "guaranteed sale price" or "guaranteed days on market" language
- No fabricated stats — every number is realtor-supplied or skipped
- Pricing Philosophy section: general approach only, not a CMA, not a specific recommendation
- Marketing Philosophy section: vague-by-default, phase-based, no specific vendors or ad budgets (per `skills/cma/references/output-style-guide.md` discipline)

### Step F — Confirmation with full template draft

Return the full drafted template for inline review. Show:

- Section list with final order + tab assignment
- Drafted prose for each section
- Photo handling notes (if testimonials reference photos)
- Past-listing data formatting

Ask: *"Here's the full draft. Anything off? Want to change voice, swap a section, edit specific copy?"*

### Step G — Refinement loop

Freeform feedback in plain English. Realtor can edit any section's prose, swap section order, add / remove sections, add / remove testimonials, add / remove past-listing entries, or change a section's emphasis or length.

Per round: apply feedback, regenerate affected sections, show updated template. Loop until approval.

Approval phrases: *"ship it" / "approved" / "save it" / "good enough" / "OK as-is" / "done" / "perfect"* or any semantic equivalent.

### Step H — Write the template file

Only after explicit approval. No partial writes at any earlier point.

Use Bash to ensure the directory exists:
```bash
mkdir -p ~/.config/realty-stack/
```

Use Write to save the template markdown. Confirm path back verbatim: *"Saved to ~/.config/realty-stack/listing-presentation-template.md. Run /listing-presentation any time you have a listing appointment — it'll fill the template for that specific seller and property."*

---

## Existing template detection at Step A

When `~/.config/realty-stack/listing-presentation-template.md` already exists, Step A asks once: *"You already have a template. Update specific sections, start fresh, or cancel?"*

- **Update** — re-runs Steps E–G for selected sections only
- **Fresh** — builds from scratch; overwrites on Step H approval
- **Cancel** — exit immediately

---

## Template file format

Location: `~/.config/realty-stack/listing-presentation-template.md`

```markdown
# Realty Stack — Listing Presentation Template for [Agent Full Name]
Captured: [ISO date]
Refined: [ISO date] ([N] rounds)

## Sections (in render order)
1. About Me [tab: Who I Am]
2. Why Hire Me [tab: Who I Am]
3. My Selling Process [tab: How I Work]
4. Marketing Philosophy [tab: How I Work]
5. Recent Track Record [tab: Track Record]
6. Testimonials [tab: Track Record]
7. Pricing Philosophy [tab: Working Together]
8. Fee Structure [tab: Working Together]
(custom sections appended below with tab assignment)

## Section: About Me
[Tab: Who I Am]
[Prose drafted in Email Voice from voice profile]

## Section: Why Hire Me
[Tab: Who I Am]
[Prose ...]

## Section: My Selling Process
[Tab: How I Work]
[Prose ...]

## Section: Marketing Philosophy
[Tab: How I Work]
[Prose ...]

## Section: Recent Track Record
[Tab: Track Record]
[Prose intro + table:]
- Address (or partial) | Sale Price | DOM | Optional note
- ...

## Section: Testimonials
[Tab: Track Record]
- "Quote text"
  — Client name (or "Verified Client") | Optional photo path
- ...

## Section: Pricing Philosophy
[Tab: Working Together]
[Prose ...]

## Section: Fee Structure
[Tab: Working Together]
[Prose ...]

## Optional fields
- headshot_override: (path, if different from brand kit headshot)

## Refinement history
- Round 1 ([date]): initial build from data dump
- Round 2 ([date]): tightened About Me, swapped Pricing Philosophy second paragraph
```

---

## Section-to-tab mapping

| Section | Tab |
|---|---|
| About Me | Tab 1 — Who I Am |
| Why Hire Me | Tab 1 — Who I Am |
| My Selling Process | Tab 2 — How I Work |
| Marketing Philosophy | Tab 2 — How I Work |
| Recent Track Record | Tab 3 — Track Record |
| Testimonials | Tab 3 — Track Record |
| Pricing Philosophy | Tab 4 — Working Together |
| Fee Structure | Tab 4 — Working Together |

Custom sections: skill proposes the most natural tab based on theme; agent confirms.

---

## Edge cases

| Situation | Behavior |
|---|---|
| Realtor has no source material (fresh build) | Skip Step B analysis; go straight to Step D with all sections marked as gaps; ask targeted questions for every section. |
| Realtor's dump covers only 2-3 of the 8 sections | Cover the rest via Step D targeted questions; flag in Step F draft which sections are "thin" so realtor can expand later. |
| Realtor wants a custom section (e.g., Community Involvement) | Add during Step D; ask which of the 4 tabs it belongs to; skill proposes the most natural tab based on theme. |
| Testimonial photo path doesn't exist | Ask for valid path or accept text-only quote. |
| Testimonial quote names protected-class info ("such a nice family of five") | Flag in Step F draft: *"This quote could read as protected-class targeting under fair housing. Want me to omit, anonymize, or trim?"* Don't auto-edit — ask. |
| Existing template at file path | Step A asks: *"You already have a template. Update specific sections / start fresh / cancel?"* (see §"Existing template detection at Step A"). |
| Onboarding interrupted | Template file isn't written until Step H. Next session, agent re-runs `/listing-presentation-template` from scratch (no half-saved state). |
| Template file corrupted | Overlay / `/listing-presentation` detects on load; re-triggers onboarding. |
| Agent wants different brand mid-build | Out of scope for v0.0.4 — finish current template with current brand; re-run `brand-kit-capture` for different-brand templates in future versions. |
| Realtor pastes voice samples instead of bio | Politely redirect: *"Voice samples are voice-draft's territory — already captured. For this skill, I need your bio / about / brokerage profile."* |
| Realtor pastes 30 past listings | Default render = top 6 by recency; agent can override during refinement. Template stores all provided entries; skill picks for display. |

---

## What this skill never does

- Fabricate stats, awards, or testimonials — every fact is realtor-supplied or skipped
- Persist anything to `~/.config/realty-stack/voice-profile.md` or `~/.config/realty-stack/brand-kit.md` — those are owned by voice-draft and brand-kit-capture
- Skip the compliance check on testimonials (always flag protected-class language)
- Auto-edit testimonials with protected-class language — flag and ask, never auto-edit
- Save before Step H approval (no partial writes)
- Mix Text Voice with Email Voice — template prose is Email Voice only
- Make pricing or DOM guarantees in Pricing Philosophy section — general approach only
- Commit to specific vendors, ad budgets, or week-numbered timelines in Marketing Philosophy — vague-by-default, phase-based
- Use a default agent or brokerage — pulls from Agent Profile in voice profile

---

✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon
