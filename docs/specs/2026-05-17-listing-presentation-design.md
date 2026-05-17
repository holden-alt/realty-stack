# v0.0.4 — Listing Presentation Skill Pair + /cma Retrofits — Design Spec

**Status:** Draft 2026-05-17. Pending Holden review.
**Author:** Holden Richardson
**Skills:** `skills/listing-presentation-template/`, `skills/listing-presentation/`
**Cross-cutting:** `/cma` tab visibility + print CSS retrofits
**Sibling skill prerequisites:** `voice-draft`, `brand-kit-capture`
**Source material:** v0.0.4 brainstorm (2026-05-17), Holden's 6333 Blackmar listing presentation, `/cma` design pattern

---

## TL;DR

A two-skill pair plus two cross-cutting retrofits to `/cma`.

**Skill pair (the listing-appointment pitch):**
- `/listing-presentation-template` — one-time consultative builder. Captures the agent's reusable pitch content (about-me, process, marketing philosophy, track record, testimonials, pricing, fees). Saves to `~/.config/realty-stack/listing-presentation-template.md`. Mirrors voice-draft + brand-kit-capture's one-time-onboarding-then-persist architecture.
- `/listing-presentation` — per-listing filler. Takes the template + light personalization (seller name, property address, appointment date, optional custom note) and produces a self-contained 4-tab HTML pitch the realtor brings to the appointment alongside a separately-run `/cma`.

**Cross-cutting `/cma` retrofits (also v0.0.4):**
- **Tab visibility upgrade.** Current `01 / OVERVIEW` mono-caption tabs read as page numbers, not buttons. Redesign as obviously-clickable tabs. Apply across `/cma` seller + buyer + new listing-presentation templates.
- **Print CSS polish.** Bulletproof `@media print` so Cmd+P → Save as PDF produces clean output. Apply across all three templates.

---

## Motivation

`/cma` is the analytical work — what's the property worth, what should we list at. But before the CMA conversation, the seller is evaluating **the agent**: Why hire you? What's your process? What's your track record? That's the "listing presentation" — the agent's pitch that earns the listing.

Generic AI doesn't help here because:
- Pitch content is high-personal and reused across listings (build once, fill per appointment — not draft from scratch every time)
- Voice has to be the realtor's, not generic
- Visual brand has to match the realtor's brand kit
- Print quality matters — agents leave a printed copy with the seller; PDFs end up in inboxes

The skill pair takes the build-once-fill-per-appointment workflow seriously. The consultative template build is a one-time investment that pays off every listing appointment after. The per-listing skill is light personalization, not re-drafting.

The /cma retrofits ship in the same cycle because both are visual-output discipline that touches every existing template — fixing them together (and codifying them in `output-style-guide.md`) means future visual skills inherit the new patterns for free.

---

## Scope

### In scope (v0.0.4)

**Sub-project A — the skill pair:**
- `/listing-presentation-template` — consultative builder (hybrid front-loaded data dump pattern)
- `/listing-presentation` — per-listing filler (template + light personalization → HTML)
- 8 standard sections, flexible (agent can add / remove / reorder; skill proposes additions from data-dump themes)
- 4-tab HTML output (Who I Am / How I Work / Track Record / Working Together)
- Optional inline `/cma` offer during `/listing-presentation` (one appointment, both artifacts)
- Template persisted at `~/.config/realty-stack/listing-presentation-template.md`
- Voice profile (Email Voice) for all prose; brand kit for all visual styling

**Sub-project D — cross-cutting `/cma` retrofits:**
- Tab visibility upgrade across `/cma` seller + buyer + new listing-presentation templates
- Print CSS polish across all three templates
- `skills/cma/references/output-style-guide.md` documents both patterns as canonical for future visual skills

### Out of scope (deferred)

**Sub-project B — buyer-presentation pair.** Deferred to v0.0.5+. `/buyer-presentation-template` + `/buyer-presentation` will derive from the same architecture after v0.0.4 ships. Defer to validate the listing-side pattern first.

**Sub-project C — artifact sharing infrastructure.** SKIPPED. Cowork handles HTML publish natively; local Claude Code users email the HTML file directly. No infrastructure to build. YAGNI win.

**Also out of scope:**
- Live template editing UI (template edits via re-running `/listing-presentation-template`)
- Per-section single-edit flow inside the per-listing skill (re-run template builder instead)
- Auto-extraction of past listings from MLS or CRM
- Auto-pull of testimonials from Zillow / Realtor.com profiles
- Multiple templates per agent (e.g., luxury vs first-time-buyer pitch) — single template in v0.0.4
- A/B variants of the template
- Real-time co-presentation tools (in-browser annotation, screen share)
- PDF generation tooling (WeasyPrint, Puppeteer) — browser print is the path

---

## Design — `/listing-presentation-template` (Sub-project A.1)

### Skill purpose

One-time consultative onboarding that captures the agent's reusable pitch content. Paid once in time; every listing appointment after benefits. Mirrors voice-draft + brand-kit-capture.

### Triggers

The skill auto-routes when the agent asks to:
- "set up my listing presentation"
- "build my listing pitch"
- "create my listing presentation template"
- "I want a listing presentation"
- "configure my listing template"
- "build my listing presentation template"

### Triggers (inline fallback)

If `/listing-presentation` is invoked and the template file doesn't exist, `/listing-presentation` runs `/listing-presentation-template` inline to completion before continuing. Same fallback pattern as `/cma` → `brand-kit-capture`.

Not auto-prompted by the SessionStart hook — template is optional (only realtors who plan to use `/listing-presentation` need it), not foundational like voice profile + brand kit.

### Voice profile + brand kit pre-checks

Before any template work, verify both pre-requisites:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline. Template prose is drafted in Email Voice (long-form professional doc).
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline. Headshot may come from brand kit assets; brand voice notes inform tone.

Same pattern as `/cma`. Never produce un-voiced or un-branded output.

### Onboarding workflow (Steps A–H)

Work through these eight steps in order. Don't write the template file until Step H.

#### Step A — Front-loaded data dump

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

Realtor pastes / drops / describes whatever they have. Skill reads PDFs via the `pages` parameter where applicable. Empty dump is valid — Step B detects and skips straight to Step D with all sections as gaps.

#### Step B — Analyze the dump

Skill categorizes dump content into the 8 standard sections:

1. **About Me** — bio, credentials, years in business, personal differentiators
2. **Why Hire Me** — value prop, what the seller gets from working with this agent
3. **My Selling Process** — phases, milestones, what happens between listing and closing
4. **Marketing Philosophy** — channels, approach to reaching buyers (NOT property-specific tactics)
5. **Recent Track Record** — recent listings, sale prices, days on market, list-to-sale ratios
6. **Testimonials** — client quotes (with or without names / photos)
7. **Pricing Philosophy** — general approach to pricing strategy (NOT a specific CMA)
8. **Fee Structure** — commission, what's included, what isn't, who pays what at closing

Skill also identifies recurring themes in the dump that suggest additional sections (e.g., "your dump mentions community involvement 5 times — want a Community / Local Specialization section?").

#### Step C — Propose the structure

Return a single confirmation message:

- Covered sections (with source material)
- Gaps (sections with no source material in the dump)
- Suggested additional sections (themes from the dump that don't fit the standard 8)
- Proposed final section list with order

Ask:
> *"Here's the structure I'd propose. Add / remove / reorder anything. For the gaps, I'll ask targeted questions to fill them in next."*

#### Step D — Confirm sections + fill gaps

Realtor confirms the section list (any edits). Skill then asks targeted questions for any section with no source material from the dump. Questions are section-specific:

- **About Me:** years licensed, brokerage, what's distinctive about your background
- **Why Hire Me:** what's different about working with you vs the agent down the street
- **My Selling Process:** walk me through what happens between "we sign the listing agreement" and "we close"
- **Marketing Philosophy:** how do you actually reach buyers — channels you use, channels you avoid
- **Recent Track Record:** past listings (addresses or partial — agent's call), prices, DOM, any standout outcomes
- **Testimonials:** paste 3-5 client quotes; note for each whether to include client name (and whether to include a photo path)
- **Pricing Philosophy:** how do you think about pricing strategy in general — aggressive, conservative, market-driven, hybrid
- **Fee Structure:** your commission %, what's included in the fee, what closing costs go to whom

Only ask for sections that have no source material. If the dump covered a section thoroughly, skip the question for that section.

#### Step E — Draft each section in Email Voice

For each section, draft prose using the realtor's Email Voice from their voice profile:

- Match sentence length patterns, opener style, signoff usage
- Use "Practical & Local" — name specific streets, neighborhoods, brokerage details, not generic descriptors
- Respect compliance:
  - No fair housing red flags ("such a nice family", neighborhood demographic descriptors)
  - No "guaranteed sale price" or "guaranteed days on market" language
  - No fabricated stats — every number is realtor-supplied or skipped
- Pricing Philosophy section: general approach only, not a CMA, not a specific recommendation
- Marketing Philosophy section: vague-by-default, phase-based, no specific vendors or ad budgets (per existing `output-style-guide.md` discipline)

#### Step F — Confirmation with full template draft

Return the full drafted template to the realtor for inline review. Show:

- Section list with final order + tab assignment
- Drafted prose for each section
- Photo handling notes (if testimonials reference photos)
- Past-listing data formatting

Ask:
> *"Here's the full draft. Anything off? Want to change voice, swap a section, edit specific copy?"*

#### Step G — Refinement loop

Freeform feedback in plain English. Realtor can:

- Edit any section's prose directly (paste new copy or describe what to change)
- Swap section order
- Add / remove sections
- Add / remove testimonials
- Add / remove past-listing entries
- Change a section's emphasis or length

Per round: apply feedback, regenerate affected sections, show updated template. Loop until approval.

Approval phrases (per `/cma` pattern): *"ship it" / "approved" / "save it" / "good enough" / "OK as-is" / "done" / "perfect"* or any semantic equivalent.

#### Step H — Write the template file

Only after explicit approval. No partial writes at any earlier point in the workflow.

- Use Bash to ensure `~/.config/realty-stack/` exists
- Use Write to save the template markdown
- Confirm path back to realtor in one line: *"Saved to ~/.config/realty-stack/listing-presentation-template.md. Run /listing-presentation any time you have a listing appointment — it'll fill the template for that specific seller and property."*

### Template file format

**Location:** `~/.config/realty-stack/listing-presentation-template.md`

**Format:**

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

**Format choice rationale:** same as voice profile + brand kit — Markdown is LLM-friendly to load, human-readable for the realtor to inspect and hand-edit, easy to version and diff.

### Edge cases & failure modes (template builder)

| Situation | Behavior |
|---|---|
| Realtor has no source material (fresh build) | Skip Step B analysis; go straight to Step D with all sections marked as gaps; ask targeted questions for every section. |
| Realtor's dump covers only 2-3 of the 8 sections | Cover the rest via Step D targeted questions; flag in Step F draft which sections are "thin" so realtor can expand later. |
| Realtor wants a custom section (e.g., Community Involvement) | Add during Step D; ask which of the 4 tabs it belongs to; skill proposes the most natural tab based on theme. |
| Testimonial photo path doesn't exist | Ask for valid path or accept text-only quote. |
| Testimonial quote names protected-class info ("such a nice family of five") | Flag in Step F draft: *"This quote could read as protected-class targeting under fair housing. Want me to omit, anonymize, or trim?"* Don't auto-edit — ask. |
| Existing template at file path | Step A asks: *"You already have a template. Update specific sections / start fresh / cancel?"* Update mode = re-runs the consultative flow for selected sections only. Fresh = builds from scratch (overwrites on Step H approval). Cancel = exit. |
| Onboarding interrupted | Template file isn't written until Step H. Next session, agent re-runs `/listing-presentation-template` from scratch (no half-saved state). |
| Template file corrupted | Overlay / `/listing-presentation` detects on load; re-triggers onboarding. |
| Agent wants different brand mid-build | Out of scope for v0.0.4 — finish current template with current brand; re-run `brand-kit-capture` for different-brand templates in future versions. |
| Realtor pastes voice samples instead of bio | Politely redirect: *"Voice samples are voice-draft's territory — already captured. For this skill, I need your bio / about / brokerage profile."* |
| Realtor pastes 30 past listings | Default render = top 6 by recency; agent can override during refinement. Template stores all provided entries; skill picks for display. |

---

## Design — `/listing-presentation` (Sub-project A.2)

### Skill purpose

Per-listing skill that takes the saved template + light per-appointment personalization (seller name, property address, appointment date, optional custom note) and produces a self-contained 4-tab HTML pitch the realtor brings to the appointment.

### Triggers

The skill auto-routes when the realtor says any of:

- "make a listing presentation for [address]"
- "listing presentation for [seller name]"
- "I have a listing appointment with [address]"
- "prepare for my listing appointment at [address]"
- "build my pitch for [address]"
- "create my listing presentation for [seller]"

### Path fork — overlap with `/cma`

Some trigger phrases overlap with `/cma` (e.g., "listing presentation for [address]"). When the realtor's intent could go either way, ask once:

> *"Want the listing pitch (the about-you / process / track-record piece) or the CMA (the numbers — what to price at)? Or both? Both = two artifacts at the same appointment."*

If "both" or "the pitch and the CMA": run `/listing-presentation` first, then offer `/cma` at Step 3.

### Pre-checks

- **Voice profile** present (Email Voice for cover greeting + custom-note framing). If missing, run `voice-draft` inline.
- **Brand kit** present (visual styling). If missing, run `brand-kit-capture` inline.
- **Listing presentation template** present at `~/.config/realty-stack/listing-presentation-template.md`. If missing, run `/listing-presentation-template` inline to completion before continuing.

### Per-listing workflow (Steps 1–5)

#### Step 1 — Collect per-listing personalization

Ask once, in one message:

> *"Tell me about this listing:*
> *- Seller name(s) — how should I greet them on the cover?*
> *- Property address*
> *- Appointment date*
> *- Optional: any custom note you want to add — a personalized intro, a referrer mention, anything specific to this seller you want called out on the cover or in About Me*
>
> *That's it — the rest comes from your template."*

#### Step 2 — Verify template freshness

Load `~/.config/realty-stack/listing-presentation-template.md`. Confirm in one line:

> *"Using your template (last refined [date], [N] sections). Want me to update anything before generating, or run it as-is?"*

If realtor wants updates: hand off to `/listing-presentation-template` (update mode for specific sections), then return here.

If "as-is": proceed.

#### Step 3 — Optional inline `/cma` offer

Ask once, terse:

> *"Want me to also run /cma for this property?"*

If yes: run `/cma` inline (full `/cma` flow — seller path, pre-flight, comps, research, draft, feedback). Outputs land in `~/Downloads/` as two files.

If no: proceed to Step 4.

#### Step 4 — Build the HTML

Load `references/html-template-listing-presentation.html`. Substitute every `{{PLACEHOLDER}}` value.

**Brand kit substitution (same as `/cma`):**
- `{{BG_COLOR}}`, `{{BG_DEEP_COLOR}}`, `{{INK_COLOR}}`, `{{INK_SOFT_COLOR}}`, `{{RULE_COLOR}}`, `{{ACCENT_COLOR}}`, `{{RED_COLOR}}`, `{{GREEN_COLOR}}` — direct hex from `brand-kit.md`
- `{{ACCENT_SOFT_COLOR}}` — derived from accent via HSL shift (lightness +25–30%, saturation –40%)
- `{{GOOGLE_FONTS_LINK}}` — full `<link>` tag for the brand kit's display + mono fonts
- `{{DISPLAY_FONT}}`, `{{MONO_FONT}}` — bare font family names
- `{{WORDMARK_LEFT}}`, `{{WORDMARK_SEPARATOR}}`, `{{WORDMARK_RIGHT}}` — three wordmark parts (CSS-styled HTML text, never image)

**Asset embedding (same as `/cma`):** headshot, logo, wordmark mark — base64-embedded inline. Never reference asset files by path.
- `{{COVER_HEADSHOT_HTML}}` — composite placeholder. Full `<img class="agent-photo" src="data:image/...;base64,...">` chunk if a headshot asset is available in the brand kit (or template `headshot_override`), otherwise empty string. Avoids a broken empty `<img>` tag if no headshot is present.
- `{{FOOTER_LOGO_HTML}}` — composite placeholder. Full `<img class="footer-logo" src="data:image/...;base64,...">` chunk if a logo asset is available, otherwise empty string.

**Composite-placeholder rationale.** For optional visual elements (headshot, logo, custom note), the template uses single composite placeholders (`{{COVER_HEADSHOT_HTML}}`, `{{FOOTER_LOGO_HTML}}`, `{{COVER_CUSTOM_NOTE_HTML}}`). The skill builds the full HTML chunk (with base64-embedded asset or actual prose) or emits empty string. This avoids broken empty `<img>` tags or empty wrapping `<p>` elements in rendered output without conditional logic in the template itself.

**Per-listing personalization:**
- `{{SELLER_NAME}}` — from Step 1
- `{{PROPERTY_ADDRESS}}` — from Step 1
- `{{APPOINTMENT_DATE}}` — from Step 1, formatted as "Tuesday, May 20, 2026"
- `{{COVER_CUSTOM_NOTE_HTML}}` — composite placeholder. If a custom note was provided in Step 1, the skill emits a full `<p class="custom-note">...</p>` chunk. If absent, the skill emits empty string. The template substitutes the chunk into the cover hero without needing conditional logic.
- `{{AGENT_NAME}}`, `{{AGENT_BROKERAGE}}`, `{{AGENT_PRIMARY_MARKET}}` — from voice profile Agent Profile section

**Section content from template:**
- `{{SECTION_LIST_TAB_1}}` — HTML for sections assigned to Tab 1 (Who I Am)
- `{{SECTION_LIST_TAB_2}}` — HTML for sections assigned to Tab 2 (How I Work)
- `{{SECTION_LIST_TAB_3}}` — HTML for sections assigned to Tab 3 (Track Record)
- `{{SECTION_LIST_TAB_4}}` — HTML for sections assigned to Tab 4 (Working Together)
- Each section renders with: section header, drafted prose, optional structured content (track-record table, testimonial cards with photos)

**Testimonial photo handling:** if a testimonial in the template references a photo path, read the file and base64-embed. If the path doesn't exist at generation time, skip silently and render text-only quote (no error to the realtor; the template captured the intent).

**Voice profile prose handling:** template prose is already drafted in Email Voice during template build. Per-listing generation does light prose-touch only — generate the cover hero greeting (e.g., "Prepared for [Seller Name]") and the optional custom-note intro framing in Email Voice. Don't re-draft template sections per listing.

**Cover hero composition:**
- Brand wordmark (CSS-rendered, top-left)
- Optional agent photo (right side, from brand kit headshot OR template `headshot_override` if set)
- "Listing Presentation for [Seller Name]" headline
- Property address
- Appointment date
- Optional custom note (small, below the address)

#### Step 5 — Write the file

No mid-flow approval gate (template was approved during build; per-listing is light personalization only). Write directly after Step 4.

- **Default output path:** `~/Downloads/<property-slug>-listing-presentation.html`. Slug is lowercased street address with non-alphanumerics replaced by hyphens (e.g., `1247-plainfield-listing-presentation.html`).
- **Path conflict:** append timestamp suffix (`<slug>-listing-presentation-2026-05-17-1430.html`). Never overwrite silently.
- **Override:** if realtor says *"save to [path]"*, honor it.

Confirm path back:
> *"Saved to ~/Downloads/1247-plainfield-listing-presentation.html — open in Chrome / Safari to preview, ⌘P prints cleanly with all tabs expanded."*

### Edge cases & failure modes (per-listing)

| Situation | Behavior |
|---|---|
| Template missing | Run `/listing-presentation-template` inline; return to original request when done. |
| Template exists but no sections defined (corrupted) | Treat as missing; run `/listing-presentation-template` inline. |
| Realtor skips the optional custom note | Render cover without the custom-note line (no empty placeholder visible). |
| Seller name as "the Smiths" instead of "John and Jane Smith" | Honor it — render exactly what's provided. Realtor knows their seller. |
| Property address ambiguous | Ask once for full street address + city; don't guess. |
| Appointment date in the past | Render anyway — realtor may be generating retroactively for record-keeping. No warning. |
| Testimonial photo path missing at generation | Skip silently, render text-only quote. |
| Inline `/cma` fails mid-flow | Save the listing-presentation file successfully; tell realtor `/cma` can be re-run separately. |
| Realtor wants different brand for this specific listing | Out of scope — uses active brand kit. |
| Output file path already exists | Append timestamp suffix; never overwrite silently. |
| Realtor mid-flow asks unrelated question | Pause gracefully, answer, offer to resume. Do not lose collected per-listing state. |

---

## Design — Cross-cutting `/cma` retrofits (Sub-project D)

Two retrofits ship in v0.0.4 alongside the new skill pair. Both touch `/cma`'s existing HTML references and the `output-style-guide.md`.

### Retrofit 1 — Tab visibility upgrade

**Problem:** `/cma`'s current tab styling uses `01 / OVERVIEW`-style mono-caption labels that read as page numbers, not buttons. Holden flagged this — sellers (and buyers, for the buyer template) miss the tabs entirely on first glance.

**Fix:** redesign the tab UI with obvious button affordances.

**New visual language:**
- Button-like background (subtle `bg-deep` fill behind each tab label, light rounded corners)
- Distinct active state (filled accent-soft background OR inverted ink/bg, with visible weight contrast)
- Clear hover state (background brightens slightly)
- Number prefix optional (keep the `01` if it helps the eye, but visually subordinate to the label)
- Mono-caption styling retained for the label text (preserves the editorial brand discipline)
- Mobile: keep the native `<select>` fallback (works as-is, no change needed)

**Where applied:**
- `skills/cma/references/html-template-seller.html`
- `skills/cma/references/html-template-buyer.html`
- `skills/listing-presentation/references/html-template-listing-presentation.html` (uses the new pattern from day 1)

**Codified in:** `skills/cma/references/output-style-guide.md` — add a "Tab affordance" section with the new CSS pattern + visual reference.

### Retrofit 2 — Print CSS polish

**Problem:** Cmd+P on current `/cma` templates produces uneven output — orphans, tabs not expanded, interactive controls (mortgage calc inputs, net-sheet inputs) visible on the printed page.

**Fix:** comprehensive `@media print` rules.

**Rules:**
- Expand ALL tabs simultaneously on print (every section's content visible, no `display: none` on inactive tabs)
- Force `page-break-inside: avoid` on section cards / accordion bodies
- Force `page-break-before: always` between major tab sections (so each tab starts on a new page)
- Hide interactive controls: `<button>`, `<input>`, `<select>`, tab nav buttons, "Show research" toggles
- Preserve background colors where critical (cover hero, accent strips) via `-webkit-print-color-adjust: exact`
- Limit page width to 7.5in (Letter with 0.5in margins)
- Force `font-family: <display>` on body for print rendering consistency
- Strip auto-appended URLs from links (`a[href]::after { content: none; }`)

**Where applied:**
- `skills/cma/references/html-template-seller.html`
- `skills/cma/references/html-template-buyer.html`
- `skills/listing-presentation/references/html-template-listing-presentation.html` (built with the new rules from day 1)

**Codified in:** `skills/cma/references/output-style-guide.md` — add a "Print compatibility" section with the canonical `@media print` block + the rationale for each rule.

---

## Architecture

```
skills/
├── listing-presentation-template/                              [NEW]
│   └── SKILL.md
├── listing-presentation/                                        [NEW]
│   ├── SKILL.md
│   └── references/
│       └── html-template-listing-presentation.html
└── cma/
    └── references/
        ├── html-template-seller.html                            [UPDATED — tab + print retrofit]
        ├── html-template-buyer.html                             [UPDATED — tab + print retrofit]
        └── output-style-guide.md                                [UPDATED — tab + print sections added]

commands/
├── listing-presentation-template.md                             [NEW — slash wrapper]
└── listing-presentation.md                                      [NEW — slash wrapper]

skills/using-realty-stack/SKILL.md                               [UPDATED — add /listing-presentation to active catalog]

VERSION                                                          [UPDATED — 0.0.4]
.claude-plugin/plugin.json                                       [UPDATED — version bump]
README.md                                                        [UPDATED — skills table]
CHANGELOG.md                                                     [UPDATED — v0.0.4 entry]

docs/specs/2026-05-17-listing-presentation-design.md             [NEW — this document]
```

**State files (runtime, not in repo):**
- `~/.config/realty-stack/listing-presentation-template.md` — created/updated by `/listing-presentation-template`

### Sibling-skill consumption

**Voice profile (`~/.config/realty-stack/voice-profile.md`).** Use Email Voice. Pulls from voice-draft. Per-listing skill uses voice for cover greeting and optional custom-note framing only — template prose is already drafted at template build time.

**Brand kit (`~/.config/realty-stack/brand-kit.md`).** All visual styling. Headshot from brand assets used in cover hero (right side, optional). Wordmark CSS-rendered. Asset files base64-embedded in output HTML.

**`/cma` (optional inline).** At Step 3 of `/listing-presentation`, ask whether to also run `/cma`. If yes, full `/cma` flow runs; outputs land in `~/Downloads/` as two files.

---

## What these skills never do

- Auto-send the presentation to clients — output is for the realtor to review and present
- Fabricate stats, awards, or testimonials — every fact is realtor-supplied or skipped
- Generate "exclusive listing," "off-market," or "private listing" language unless realtor explicitly confirms the listing has that status (per CLAUDE.md Do-Not)
- Use a default brand or anyone else's brand — always the active brand kit, or run `brand-kit-capture` inline first
- Mix Text Voice with Email Voice — template prose and cover greeting are Email Voice only
- Persist anything to `~/.config/realty-stack/voice-profile.md` or `~/.config/realty-stack/brand-kit.md` — those are owned by `voice-draft` and `brand-kit-capture`
- Embed protected-class targeting language in testimonials — flag and ask before omitting / anonymizing / trimming
- Make pricing or DOM guarantees in Pricing Philosophy section — general approach only
- Commit to specific vendors, ad budgets, or week-numbered timelines in Marketing Philosophy — vague-by-default, phase-based, per `output-style-guide.md`
- Reference asset files by path in HTML output — always base64-embed (breaks self-containment otherwise)
- Use the accent / brass color as a background fill — pigment-only, per existing design discipline

---

## Implementation surface

### New
- `skills/listing-presentation-template/SKILL.md` — consultative builder workflow (Steps A–H)
- `skills/listing-presentation/SKILL.md` — per-listing filler workflow (Steps 1–5)
- `skills/listing-presentation/references/html-template-listing-presentation.html` — 4-tab parameterized template (new tab affordance + print CSS from day 1)
- `commands/listing-presentation-template.md` — slash command wrapper
- `commands/listing-presentation.md` — slash command wrapper
- `docs/specs/2026-05-17-listing-presentation-design.md` — this document

### Modified
- `skills/cma/references/html-template-seller.html` — tab affordance + print CSS retrofit
- `skills/cma/references/html-template-buyer.html` — tab affordance + print CSS retrofit
- `skills/cma/references/output-style-guide.md` — new "Tab affordance" + "Print compatibility" sections
- `skills/using-realty-stack/SKILL.md` — add `/listing-presentation` to active catalog; `/listing-presentation-template` is one-time onboarding (not always-active)
- `.claude-plugin/plugin.json` — version bump
- `VERSION` — 0.0.3 → 0.0.4
- `README.md` — add skills to table
- `CHANGELOG.md` — v0.0.4 entry covers both new skills + both retrofits

### Unchanged
- `voice-draft`, `brand-kit-capture`, `/cma` SKILL.md body (only `/cma`'s HTML references + style guide change)
- `knowledge/` files (voice-guide, constitution, fair-housing all continue)
- `hooks/` — no SessionStart change; `/listing-presentation-template` is invoked by trigger phrase or `/listing-presentation` fallback, not auto-prompted
- ETHOS, CONTRIBUTING, SECURITY, LICENSE, CLAUDE.md (no contract change — listing-presentation template is consumer-only of voice + brand contracts)

---

## Open questions for the implementation plan

None blocking design. Implementation-detail decisions for `writing-plans`:

1. **Tab affordance exact CSS.** Direction is settled (button-like, distinct active state). Specific CSS (border-radius value, hover transition timing, active-state color rule) is a designer call during implementation. Recommend prototyping on the seller template first, then porting to buyer + listing-presentation.

2. **Print CSS exact rules.** Direction is clear (expand all, page breaks between tabs, hide controls). Specific rule order, browser-prefix handling, and `-webkit-print-color-adjust` exceptions are an implementation detail. Recommend writing the rules as a shared partial that all three HTML files include via `<style>` block copy (template-substitution makes a literal include awkward without a build step).

3. **Update vs fresh template mode (Step A).** When existing template is detected, flow needs three paths: update-specific-sections, start-fresh, cancel. Update mode = re-runs the consultative flow for selected sections only. Fresh = builds from scratch (overwrites on Step H). Detail the update-mode UX during implementation.

4. **Custom section tab assignment.** When agent adds a custom section, skill proposes the most natural tab based on theme. Lean: LLM classifies the section's theme against the 4 tab themes (Who I Am / How I Work / Track Record / Working Together) and proposes; agent confirms.

5. **Past-listing render count default.** How many entries surface in Track Record by default. Lean: top 6 by recency, agent can override during template refinement.

6. **Agent photo source priority.** Default to brand kit headshot if present. Allow template to override (e.g., agent uses a different photo for listing presentations vs other materials) via optional `headshot_override` field in the template format.

7. **Section assignment-to-tab encoding in template.** Template format uses `[Tab: <name>]` after each section header. Validation: at template-write time, verify every section has a valid tab assignment from the 4 standard tab names. Reject malformed entries.

8. **Mobile fallback styling for new tab affordance.** Existing `/cma` uses native `<select>`. Confirm the new tab affordance preserves that fallback (probably yes — the `<select>` is the mobile substitute regardless of desktop tab styling).

9. **`/cma` inline offer copy.** Exact wording for the optional `/cma` offer at Step 3 of `/listing-presentation`. Lean: keep terse — *"Want me to also run /cma for this property?"*

10. **HTML parameterization style.** Same `{{PLACEHOLDER}}` pattern as `/cma`. Confirm during implementation that no clever new format is needed.

---

## Success criteria

The skill pair + retrofits are working when:

1. Holden can run `/listing-presentation-template` from a fresh state and capture a complete reusable template in under 30 minutes of consultative flow.
2. Per-listing `/listing-presentation` produces a presentation-ready HTML file in under 5 minutes from invocation to file written.
3. The HTML output looks visually identical in spirit to a high-end listing presentation but styled to the agent's brand kit.
4. Cmd+P → Save as PDF produces clean output across all three templates (seller `/cma`, buyer `/cma`, listing-presentation): all tabs expanded, no orphans, interactive controls hidden, backgrounds preserved where intended.
5. Tabs are obviously clickable on first sight — a non-realtor opening the HTML sees a tab and knows to click. (Visual user test, not automated.)
6. Voice in template prose passes the realtor's gut check on first generate ("sounds like me").
7. The skill pair pattern (template builder + per-instance filler) is reusable enough that v0.0.5's `/buyer-presentation-template` + `/buyer-presentation` can be derived with minimal new design.
8. Output files land at the documented path and open cleanly in Chrome / Safari / iOS Safari / Android Chrome.

---

## Next step

After approval: invoke `superpowers:writing-plans` to produce the implementation plan. Likely one combined plan covering:

- Sub-project A.1 — `/listing-presentation-template` SKILL.md + commands wrapper
- Sub-project A.2 — `/listing-presentation` SKILL.md + commands wrapper + HTML template
- Sub-project D.1 — `/cma` template tab visibility retrofit (seller + buyer)
- Sub-project D.2 — `/cma` template print CSS retrofit (seller + buyer)
- Sub-project D.3 — `output-style-guide.md` update (tab + print patterns)
- Plugin / version bumps + README + CHANGELOG
- e2e test (Holden builds his real template, generates a sample listing presentation, verifies HTML + PDF)
- GitHub push v0.0.4 (explicit gate per standing rule)

Estimated 12–18 tasks. After plan approval, hand off to `superpowers:subagent-driven-development` for execution.
