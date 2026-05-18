---
name: buyer-presentation-template
description: This skill should be used when a real estate agent asks to "set up my buyer presentation", "build my buyer pitch", "create my buyer presentation template", "I want a buyer presentation", "configure my buyer template", or "build my buyer presentation template". One-time consultative builder that captures the agent's reusable buyer-side pitch content (about-me, why-hire-me, buying-process, how-i-find-homes, track-record, testimonials, negotiation-philosophy, buyer-rep-agreement) and persists to ~/.config/realty-stack/buyer-presentation-template.md so per-listing /buyer-presentation can render in seconds.
version: 0.0.1
---

# Buyer Presentation Template — Build Once, Fill Per Appointment

One-time consultative onboarding that captures the agent's reusable BUYER pitch content (vs `/listing-presentation-template` which captures the SELLER pitch). Sibling to `/cma`'s buyer path. About the AGENT — how I work with buyers, my buying process, my track record, my fee structure. Paid once in time; every buyer appointment after benefits.

---

## When this skill runs

Trigger phrases:

- "set up my buyer presentation"
- "build my buyer pitch"
- "create my buyer presentation template"
- "I want a buyer presentation"
- "configure my buyer template"
- "build my buyer presentation template"

**Inline fallback:** `/buyer-presentation` runs this skill inline if `~/.config/realty-stack/buyer-presentation-template.md` is missing, then returns to the per-appointment request.

---

## Voice profile + brand kit pre-checks

Before any template work, verify both pre-requisites:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion. Template prose is drafted in Email Voice (long-form professional doc).
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion. Headshot may come from brand kit assets; brand voice notes inform tone.

Pattern matches `/cma`. Never produce un-voiced or un-branded output.

---

## Onboarding workflow

Work through Steps 0 through H in order. Do not write the template file until Step H.

### Step 0 — State scan

Before asking the realtor for material, scan canonical realty-stack state locations per CLAUDE.md State scan contract:

```bash
ls ~/.config/realty-stack/voice-profile.md ~/.config/realty-stack/brand-kit.md \
   ~/.config/realty-stack/listing-presentation-template.md 2>/dev/null
ls ~/Downloads/*-listing-presentation.{html,pdf} ~/Downloads/*-cma.{html,pdf} \
   ~/Downloads/*-presentation.{html,pdf} 2>/dev/null
```

Build an inventory of what was found. The key inheritance opportunity: **listing-presentation-template**.

**If `listing-presentation-template.md` is found**, offer inheritance:

> *"Found your listing-presentation-template — that's a head start. I can pull these sections from it (they translate directly to the buyer side):*
> *- About Me (100% reusable — same agent, same story)*
> *- Why Hire Me (90% reusable — light edit pass for buyer-side framing)*
> *- Recent Track Record (75% reusable — you may have separate buyer-side closings to swap in)*
> *- Testimonials (90% reusable — you'll decide per-quote which translate from seller-side)*
>
> *That covers 4 of the 8 standard buyer-side sections. For the buyer-specific ones (My Buying Process, How I Find Homes, Negotiation Philosophy, Buyer Rep Agreement), I'll ask targeted questions in Step D.*
>
> *Want me to pre-populate from listing-pres-template, or start fresh with the full Step A data dump?"*

If realtor accepts inheritance: pre-populate the 4 sections with inherited content. Mark them as inherited in any refinement loop (Step F/G). Proceed to Step D for the 4 remaining buyer-specific sections — skip the Step A data dump for covered sections.

If realtor wants to start fresh: skip the inheritance, fall through to Step A.

**If nothing inheritable is found:** fall through silently to Step A.

### Step A — Front-loaded data dump (fallback for sections not inherited at Step 0)

Ask once, in a single message:

> *"To build your buyer presentation, I need everything you already have about your business. Drop anything that's relevant — paste, attach, or describe:*
>
> *- Old buyer presentations (PDF or text)*
> *- Your bio (website 'About' page, brokerage profile)*
> *- Testimonials (with or without client names — your call)*
> *- Sample buyer-side closings you'd showcase (addresses, prices, days from offer to accept)*
> *- Your brokerage's buyer-side marketing assets (if any)*
> *- Headshot / professional photo (if not already in brand kit)*
> *- Any awards, certifications, sales stats, or recognition*
> *- Stories about your process — what you actually do for buyers*
>
> *Don't worry about organizing it. I'll sort it. If you're starting fresh and have nothing, that's fine too — I'll ask targeted questions instead."*

Realtor pastes / drops / describes. Read PDFs via the Read tool's `pages` parameter where applicable. Empty dump is valid — Step B detects and skips straight to Step D with all sections as gaps.

### Step B — Analyze the dump

Categorize dump content into the 8 standard buyer-side sections:

1. **About Me** — bio, credentials, years in business, personal differentiators
2. **Why Hire Me** — value prop, what the buyer gets from working with this agent
3. **My Buying Process** — phases from initial consult through closing (offer prep, showings, inspection, financing, closing)
4. **How I Find Homes** — search philosophy, off-market access, alert systems, neighborhood expertise
5. **Recent Track Record** — recent buyer-side closings, average savings vs list, days from offer to accept
6. **Testimonials** — buyer client quotes
7. **Negotiation Philosophy** — general approach to writing offers and negotiating on the buyer side
8. **Buyer Representation Agreement** — commission/buyer-rep terms, what's included, when fees are due

Also identify recurring themes that suggest additional custom sections (e.g., "your dump mentions relocation clients 4 times — want a Relocation Specialist section?").

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
- **Why Hire Me:** what's different about working with you vs the agent down the street, buyer-side
- **My Buying Process:** walk me through what happens between "we sign the buyer-rep agreement" and "we close"
- **How I Find Homes:** what channels do you use beyond MLS — off-market, neighbor outreach, agent network
- **Recent Track Record:** past buyer-side closings (addresses or partial), purchase prices, days from offer to accept, savings achieved
- **Testimonials:** paste 3-5 buyer client quotes; note for each whether to include client name (and photo path)
- **Negotiation Philosophy:** how do you think about offer strategy in general — aggressive opening / escalation clauses / when to walk
- **Buyer Representation Agreement:** your buyer-side commission %, what's included in the fee, who pays (seller-paid vs buyer-paid)

Skip any section the dump or inheritance covered thoroughly.

### Step E — Draft each section in Email Voice

**Load `knowledge/voice-guide.md`** before drafting any section — the 6 brand voice tenets shape every prose decision and are non-negotiable per CLAUDE.md design principle 1.

For each section, draft prose using the realtor's Email Voice from their voice profile:

- Match sentence length patterns, opener style, signoff usage
- Use "Practical & Local" — name specific neighborhoods, brokerage details, not generic descriptors

**COMPLIANCE DISCIPLINE:**

- No fair housing red flags ("such a nice family", neighborhood demographic descriptors)
- No "guaranteed purchase price" or "guaranteed days to close" language
- No fabricated stats — every number is realtor-supplied or skipped
- Negotiation Philosophy section: general approach only, not a specific offer strategy
- Buyer Representation Agreement section: transparent on commission structure only; no overpromising on what fee includes

### Step F — Confirmation with full template draft

Return the full drafted template for inline review. Show:

- Section list with final order + tab assignment
- Drafted prose for each section
- Photo handling notes (if testimonials reference photos)
- Past buyer-side closing data formatting
- **Clearly mark inherited content** (sections pulled from listing-pres-template at Step 0)

Ask: *"Here's the full draft. Anything off? Want to change voice, swap a section, edit specific copy?"*

### Step G — Refinement loop

Freeform feedback in plain English. Realtor can edit any section's prose, swap section order, add / remove sections, add / remove testimonials, add / remove past-closing entries, or change a section's emphasis or length.

Per round: apply feedback, regenerate affected sections, show updated template. Loop until approval.

Approval phrases: *"ship it" / "approved" / "save it" / "good enough" / "OK as-is" / "done" / "perfect"* or any semantic equivalent.

### Step H — Write the template file

Only after explicit approval. No partial writes at any earlier point.

Use Bash to ensure the directory exists:
```bash
mkdir -p ~/.config/realty-stack/
```

Use Write to save the template markdown. Confirm path back verbatim: *"Saved to ~/.config/realty-stack/buyer-presentation-template.md. Run /buyer-presentation any time you have a buyer presentation — it'll fill the template for that specific buyer."*

---

## Existing template detection at Step A

When `~/.config/realty-stack/buyer-presentation-template.md` already exists, Step A asks once: *"You already have a template. Update specific sections, start fresh, or cancel?"*

- **Update** — re-runs Steps E–G for selected sections only
- **Fresh** — builds from scratch; overwrites on Step H approval
- **Cancel** — exit immediately

---

## Template file format

Location: `~/.config/realty-stack/buyer-presentation-template.md`

```markdown
# Realty Stack — Buyer Presentation Template for [Agent Full Name]
Captured: [ISO date]
Refined: [ISO date] ([N] rounds)

## Sections (in render order)
1. About Me [tab: Who I Am]
2. Why Hire Me [tab: Who I Am]
3. My Buying Process [tab: How I Work]
4. How I Find Homes [tab: How I Work]
5. Recent Track Record [tab: Track Record]
6. Testimonials [tab: Track Record]
7. Negotiation Philosophy [tab: Working Together]
8. Buyer Representation Agreement [tab: Working Together]
(custom sections appended below with tab assignment)

## Section: About Me
[Tab: Who I Am]
[Prose drafted in Email Voice from voice profile]

## Section: Why Hire Me
[Tab: Who I Am]
[Prose ...]

## Section: My Buying Process
[Tab: How I Work]
[Prose ...]

## Section: How I Find Homes
[Tab: How I Work]
[Prose ...]

## Section: Recent Track Record
[Tab: Track Record]
[Prose intro + table:]
- Address (or partial) | Purchase Price | Days Offer→Accept | Optional note
- ...

## Section: Testimonials
[Tab: Track Record]
- "Quote text"
  — Client name (or "Verified Client") | Optional photo path
- ...

## Section: Negotiation Philosophy
[Tab: Working Together]
[Prose ...]

## Section: Buyer Representation Agreement
[Tab: Working Together]
[Prose ...]

## Optional fields
- headshot_override: (path, if different from brand kit headshot)

## Refinement history
- Round 1 ([date]): initial build (inherited 4 sections from listing-presentation-template, drafted 4 from gap-fill)
- Round 2 ([date]): tightened How I Find Homes, swapped Negotiation Philosophy second paragraph
```

---

## Section-to-tab mapping

| Section | Tab |
|---|---|
| About Me | Tab 1 — Who I Am |
| Why Hire Me | Tab 1 — Who I Am |
| My Buying Process | Tab 2 — How I Work |
| How I Find Homes | Tab 2 — How I Work |
| Recent Track Record | Tab 3 — Track Record |
| Testimonials | Tab 3 — Track Record |
| Negotiation Philosophy | Tab 4 — Working Together |
| Buyer Representation Agreement | Tab 4 — Working Together |

Custom sections: skill proposes the most natural tab based on theme; agent confirms.

---

## Edge cases

| Situation | Behavior |
|---|---|
| Realtor has no source material (fresh build) | Skip Step B analysis; go straight to Step D with all sections marked as gaps; ask targeted questions for every section. |
| Dump covers only 2-3 of the 8 sections | Cover the rest via Step D targeted questions; flag in Step F draft which sections are "thin" so realtor can expand later. |
| Realtor wants a custom section (e.g., Relocation Specialist) | Add during Step D; ask which of the 4 tabs it belongs to; skill proposes the most natural tab based on theme. |
| Testimonial photo path doesn't exist | Ask for valid path or accept text-only quote. |
| Testimonial quote names protected-class info ("such a nice family of five") | Flag in Step F draft: *"This quote could read as protected-class targeting under fair housing. Want me to omit, anonymize, or trim?"* Don't auto-edit — ask. |
| Existing template at file path | Step A asks: *"You already have a template. Update specific sections / start fresh / cancel?"* (see §"Existing template detection at Step A"). |
| Onboarding interrupted | Template file isn't written until Step H. Next session, agent re-runs `/buyer-presentation-template` from scratch (no half-saved state). |
| Template file corrupted | Overlay / `/buyer-presentation` detects on load; re-triggers onboarding. |
| Agent wants different brand mid-build | Out of scope for v0.0.5 — finish current template with current brand; re-run `brand-kit-capture` for different-brand templates in future versions. |
| Realtor pastes voice samples instead of bio | Politely redirect: *"Voice samples are voice-draft's territory — already captured. For this skill, I need your bio / about / brokerage profile."* |
| Realtor pastes 30 past buyer-side closings | Default render = top 6 by recency; agent can override during refinement. Template stores all provided entries; skill picks for display. |

---

## What this skill never does

- Fabricate stats, awards, or testimonials — every fact is realtor-supplied or skipped
- Persist anything to `~/.config/realty-stack/voice-profile.md`, `~/.config/realty-stack/brand-kit.md`, or `~/.config/realty-stack/listing-presentation-template.md`
- Skip the compliance check on testimonials (always flag protected-class language)
- Auto-edit testimonials with protected-class language — flag and ask, never auto-edit
- Save before Step H approval (no partial writes)
- Mix Text Voice with Email Voice — template prose is Email Voice only
- Make purchase-price or savings guarantees in Negotiation Philosophy — general approach only
- Misrepresent the buyer-rep commission structure or who pays — transparent only
- Use a default agent or brokerage — pulls from Agent Profile in voice profile
- Generate "exclusive listing" / "off-market" / "private listing" language — this template is buyer-side reusable content; those listing-side terms belong in /listing-presentation output where the realtor confirms status per-appointment

---

✨ Realty Stack v0.0.5 — Realty Brain (FUB-powered always-on AI) coming soon
