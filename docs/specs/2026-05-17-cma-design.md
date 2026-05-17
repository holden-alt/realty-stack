# /cma — Design Spec

**Status:** Approved 2026-05-17. Ready for implementation plan.
**Author:** Holden Richardson
**Skill:** `skills/cma/`
**Sibling skill prerequisite:** `brand-kit-capture` (see `2026-05-17-brand-kit-capture-design.md`)
**Source material:** Holden's 6333 Blackmar listing presentation + the `listing-presentation-skill-spec.md` Holden authored from that build

---

## TL;DR

A single skill that produces a self-contained branded HTML presentation: **4-tab listing presentation for sellers, 3-tab offer strategy for buyers**. URAR-aligned sales-comparison methodology, calibrated adjustment library, weighted reconciliation, live nationwide research for state-specific tax / title / mortgage / market data. Pre-flight conversation calibrates aggressiveness; post-write feedback loop lets the realtor turn every knob (drop a comp, edit adjustments, edit weights, edit recommendation). Built on a structural philosophy the realtor knows the value and the analysis backs up their professional opinion.

---

## Motivation

CMAs are the single highest-stakes deliverable a realtor produces. They're the moment of truth at listing appointments (win or lose the listing) and the foundation of every offer strategy. Generic AI CMA tools fail because they:
- Produce numbers without backing methodology that survives client scrutiny
- Don't capture local market nuance (state tax rules, school district swings, regional convention)
- Don't support the realtor's professional opinion — they fight it
- Don't produce branded, presentation-ready output

The `/cma` skill produces output that:
- Looks like a working appraiser's URAR-style analysis
- Cites every researched number inline (verifiable)
- Bends to the realtor's professional judgment (knobs at every stage)
- Ships as a self-contained HTML the realtor can present on laptop, tablet, or phone

---

## Scope

### In scope (v0.0.3)
- Single skill, two paths (seller / buyer), forked by an early clarifying question
- 4-tab seller listing presentation: Overview, CMA, Net Sheet, Marketing
- 3-tab buyer offer strategy: Scenarios, Math, Mortgage Calculator
- URAR-aligned 20+ line-item adjustment grid
- Calibrated rate library (generic-Midwest-rural defaults; agent overrides via post-write feedback)
- Weighted reconciliation with net-adjustment-percentage reliability gates
- Aggressive vs conservative calibration knob (affects framing, weighting, and adjustment-range picks consistently)
- Live web research per invocation for state-specific math (no hardcoded state files)
- Pre-flight conversation (different question set per path)
- Post-write feedback loop (multi-round, until "ship it")
- Self-contained HTML output (mobile-responsive, brand-kit-styled, interactive net sheet / mortgage calc)
- Consumes voice profile (for prose copy) and brand kit (for visual styling) via the overlay

### Out of scope (deferred)
- PDF export (HTML print stylesheet handles printing; PDF generation is a Realty Brain feature)
- Embedded property photos (agent can add post-generation)
- Map embeds
- Cost Approach valuation (alternative methodology — not standard for residential)
- Income Approach (rental/commercial)
- Adjustment summary visual charts
- Auto-pull comps from MLS API (no MLS API integration in v0.0.3; realtor provides comp data manually or via MLS detail PDF)

---

## Design

### Skill purpose

One skill, two output paths. Forks on the first clarifying question (seller or buyer). Produces a downloadable HTML file the realtor presents.

### Triggers

The skill auto-routes when the user (a realtor) asks for any of:
- "I need to create a CMA for [client / address]"
- "Run a CMA on [address]"
- "Comparative market analysis for [address]"
- "Comp [address]"
- "Help me prepare for a listing appointment at [address]"
- "What's a fair offer on [address]"
- "Offer strategy for [address]"
- "Should my buyer offer [X] for [address]"
- "Net sheet for [address]"
- "Listing proposal for [address]"
- Any combination of the above

### Invocation flow

```
1. Trigger fires → skill loads
2. Clarify: buyer or seller? (skip if obvious from trigger phrasing)
3. Pre-flight questions (path-specific — below)
4. Collect inputs (subject + comps + condition ratings + corrections)
5. Live research phase (state tax math, title insurance schedule, market appreciation,
   school district rankings, mortgage rates if buyer-side, area property tax %,
   area HO insurance estimate if buyer-side)
6. Run analysis (URAR-aligned adjustments, weighted reconciliation)
7. Produce draft HTML output
8. Show to realtor + post-write feedback loop ("feel right? anything off?")
9. Iterate based on realtor edits — drop comp, edit adjustment, edit weight,
   edit recommendation, edit narrative, etc.
10. Approval → write final HTML to disk → confirm path
```

### Pre-flight questions

**Both paths:**
- Aggressive or conservative calibration? (affects narrative framing, comp weighting, and adjustment values picked from rate ranges — all three layers shift consistently)

**Seller-only:** none additional beyond the above

**Buyer-only:**
- Market situation for this property: sitting unsold? Just hit market? Multiple offers already? Cooling?
- Buyer constraints: hard ceiling? Willing to stretch?
- Buyer aggression tolerance: max-aggressive to win, or conservative offer?
- Locally-appropriate terms beyond price (open question — realtor enumerates what's normal locally: escalation clauses, appraisal waivers, seller closing-cost coverage, etc.)
- How many scenarios to model and how to frame them

### Required inputs

**Subject property:**
- MLS detail PDF (skill reads via Read tool's `pages` parameter) OR pasted structured data
- Must include: address, city, county, state, year built, GLA above grade, GLA below grade (finished + unfinished), bed count, bath count (full + half), lot acres, construction type, HVAC system, water/sewer, garage configuration, outbuildings, pool, school district, prior SEV / tax history, prior listing history

**Comparable sales:**
- 3-5 comps (more = better triangulation, diminishing returns past 5)
- Same data shape as subject

**Condition ratings:**
- 1-10 scale (1 = brand new, 10 = teardown)
- Required for subject AND every comp
- Not derivable from MLS — skill explicitly asks the realtor

**Property corrections (cascading):**
- MLS data is often stale — before the first draft, skill asks the realtor to verify:
  - Bath count (huge adjustment driver)
  - HVAC system + central AC
  - Recent renovations (kitchen, baths, mechanicals)
  - Basement/foundation
  - Any other facts the realtor knows differ from MLS
- Corrections cascade through every comp's adjustment grid — locked before analysis runs

### Methodology

**Sales Comparison Approach (URAR-aligned).** Federal appraisal standard. Every comparable is adjusted line-by-line for differences from the subject, producing an "adjusted value" that represents what the comp would have sold for if it had been the subject.

**Adjustment convention:**
- Positive = comp is *inferior* to subject in that line → add to comp's sale price
- Negative = comp is *superior* to subject in that line → subtract from comp's sale price
- Adjusted value = comp sale price + net adjustments

**Adjustment line items (20+, per `references/cma-methodology.md`):**
Time/Market, School District, Acreage, Effective Age, Condition, GLA, Below Grade, Bedrooms, Full Baths, Half Baths, Garage, HVAC, Fireplaces, Kitchen, Pool/Spa, Outbuildings, Recreational Features (trails/hunting), Waterfront, Construction Quality, In-Law Suite, Other Specials.

**Rate library:** generic-Midwest-rural defaults with ranges (per the calibrated table Holden built from the 6333 Blackmar work). Aggressive/conservative knob picks from top vs bottom of each range. Full rate table lives in `references/cma-methodology.md`.

**Weighting reconciliation:**
- Best GLA match + recent + same county: 25-30%
- Most recent sale: 25-30%
- Acreage match but smaller home: 10-15%
- Distant or dissimilar but bracketing: 10-15%
- High gross adjustment (>30%): 5-10%
- Net adjustment >25% = low reliability flag

Aggressive/conservative knob also shifts weights (aggressive weights higher-priced and more recent comps; conservative weights similar and cheaper).

**Final opinion of value (3 numbers):**
- Indicated value range (5th-95th percentile of comps)
- Recommended list / offer (knob-influenced: aggressive +3-5% above reconciled, conservative at-or-below)
- Probable sale / acceptance range

### Architecture

```
skills/cma/
├── SKILL.md                          # workflow (target ~400 lines)
├── references/
│   ├── cma-methodology.md            # full adjustment library, rate ranges, weighting
│   ├── html-template-seller.html     # 4-tab parameterized template
│   ├── html-template-buyer.html      # 3-tab parameterized template
│   ├── output-style-guide.md         # design system, brand discipline, mobile patterns
│   └── research-prompts.md           # canonical WebSearch queries for the research phase
└── scripts/
    ├── calc-net-sheet.py             # takes researched rates as input, does math
    ├── calc-mortgage.py              # takes researched rates as input, does math
    └── adjustment-engine.py          # consistent agg/cons knob application across rate ranges
```

### Sibling-skill consumption

**Voice profile** (via `using-realty-stack` overlay):
- Used for ALL prose copy in the output: executive summary, strategic takeaway, marketing pillars narrative, reconciliation notes, pullquotes, disclosure language
- Uses Email Voice mode (CMAs are long-form professional documents)
- Agent's name, brokerage, primary market come from Agent Profile section

**Brand kit** (via overlay, requires `brand-kit-capture` skill):
- Used for visual styling: colors, fonts, wordmark, optional logo/headshot assets
- Logo + headshot assets base64-embedded in HTML output for true self-containment
- Wordmark rendered as CSS-styled HTML text
- If brand kit is missing when /cma fires, skill detects and runs brand-kit-capture inline (same fallback pattern as voice-draft)

### Research phase

Before drafting, skill runs WebSearch + WebFetch to pull:
- State transfer tax rate (state + county-level)
- State owner's title insurance schedule
- State tax-uncapping rules (or equivalent reassessment-on-sale rules)
- Local market appreciation rate (Redfin / Zillow MSA data)
- School district rankings (PublicSchoolReview / SchoolDigger / GreatSchools / US News — use at least two sources)
- Buyer-side: current 30-year fixed mortgage rate
- Buyer-side: area property tax %
- Buyer-side: area homeowner's insurance estimate

**Caching:** results cached within the session — multiple comps share lookups.

**Citation requirement:** every researched number in the output is sourced inline (e.g., "MI State Transfer Tax (SRETT) per MCL 207.502, $3.75 per $500"). Realtor can verify before presenting.

**Failure handling:** if research returns inconclusive results for a critical value, skill asks the realtor directly: *"Couldn't find a definitive answer on [X] — what's standard in [area]?"*

### Post-write feedback loop

After producing the draft, skill prompts: *"Feel right? Anything off?"*

Realtor can adjust any of:
- Drop a comp (re-runs reconciliation)
- Add a new comp (collects data + condition rating, re-runs reconciliation)
- Edit any specific adjustment value
- Edit comp weights manually (re-runs reconciliation)
- Edit the final recommendation directly (skill keeps the math, just updates the number + narrative around it)
- Add a custom disclosure
- Re-run with aggressive/conservative knob in the other direction

Loop continues until realtor says "ship it" / "looks good" / "done" / "save it" / "approved" / semantic equivalent.

### Output

**Format:** self-contained HTML file. Mobile-responsive (native `<select>` for mobile navigation, never horizontal-scroll tabs). Interactive net sheet (seller) or mortgage calculator (buyer). Wordmark + brand-kit-styled. Logo/headshot assets base64-embedded.

**Default output location:** `~/Downloads/<property-slug>-presentation.html` — cross-platform-friendly, easy to find. Realtor can override per invocation with explicit instruction ("save to [X]").

**Print compatibility:** HTML includes `@media print` rules that expand all tabs/accordions, force page breaks between sections, hide interactive controls.

### State / regional coverage

**Works in all 50 states from day 1.** No hardcoded state-specific knowledge files. Live research per invocation handles state and county-level variation in transfer tax, title insurance, tax reassessment, and market conditions.

Realtor is licensed and responsible — verifies citations before presenting. Skill is researching, not asserting authority on tax law.

### Things this skill explicitly does NOT do

- Auto-send anything to clients (output is for realtor to review + present)
- Fabricate market data — always pulls from live web research OR asks the agent
- Skip the corrections cascade (locks facts before first draft so adjustments stay consistent)
- Commit the realtor to specific vendor names, ad budgets, or weekly milestones in the marketing tab (vague-by-default; phase-based, not week-numbered)
- Pre-suggest regionally-variable offer terms (escalations, appraisal waivers, CC coverage) — agent enumerates
- Quietly choose aggressive vs conservative — always asks
- Present numbers without inline citations (every researched value sourced)
- Skip the research phase
- Hardcode state-specific tax math
- Run without a voice profile (falls back to inline voice-draft onboarding)
- Run without a brand kit (falls back to inline brand-kit-capture onboarding)

### Edge cases & failure modes

| Situation | Behavior |
|---|---|
| Fewer than 3 comps provided | Push back: *"3 minimum for triangulation. Got 2 more I can look at?"* Don't analyze on insufficient data. |
| More than 5 comps provided | Use top 5 by similarity (auto-select); explain choice; realtor can swap during feedback loop. |
| Condition rating not provided | Always ask explicitly — never infer. *"Quick 1-10 condition rating for the subject and each comp? 1 = brand new, 10 = teardown."* |
| MLS PDF unreadable / corrupted | Ask for pasted structured data as fallback. |
| Research phase fails for critical state-tax value | Ask realtor directly; document the source-of-truth in the output ("Per realtor input — verify against current state law"). |
| Realtor refuses corrections cascade ("just use the MLS data") | Honor it; flag in caveats section: *"Adjustments based on MLS data as-provided. Verify against current property condition before presenting."* |
| Realtor wants to change brand mid-CMA | Out of scope — finish current CMA with current brand; re-run brand-kit-capture if they want a different brand for next CMA. |
| Realtor mid-CMA asks unrelated question | Pause gracefully, answer the question, offer to resume. |
| Output file path already exists | Append timestamp suffix: `<slug>-presentation-2026-05-17-1430.html` |

---

## Implementation surface (what changes in the repo)

### New
- `skills/cma/SKILL.md` — the workflow
- `skills/cma/references/cma-methodology.md` — adjustment library + rates + weighting
- `skills/cma/references/html-template-seller.html` — 4-tab parameterized template
- `skills/cma/references/html-template-buyer.html` — 3-tab parameterized template
- `skills/cma/references/output-style-guide.md` — design discipline (lifted from Holden's spec doc)
- `skills/cma/references/research-prompts.md` — WebSearch query patterns
- `skills/cma/scripts/calc-net-sheet.py` — parameterized net sheet math
- `skills/cma/scripts/calc-mortgage.py` — mortgage calculator with researched defaults
- `skills/cma/scripts/adjustment-engine.py` — agg/cons knob application
- `docs/specs/2026-05-17-cma-design.md` — this document

### Modified
- `.claude-plugin/plugin.json` — bump version, no manifest changes needed (skills auto-discovered)
- `skills/using-realty-stack/SKILL.md` — add `/cma` to the active skill catalog
- `README.md` — add CMA to the skills table
- `CHANGELOG.md` — v0.0.3 entry
- `VERSION` — bump to 0.0.3

### Unchanged
- voice-draft skill (continues working as-is)
- knowledge/ files (voice-guide, constitution, fair-housing all continue)
- ETHOS, CONTRIBUTING, SECURITY, LICENSE

---

## Open questions for the implementation plan

None blocking design. Implementation-detail decisions for `writing-plans`:

1. **HTML template parameter format.** Template uses placeholders like `{{BRAND_PRIMARY_COLOR}}` — Mustache-style? Jinja-style? Simple string replace? Pick one.
2. **adjustment-engine.py interface.** Pure function input/output shape — needs concrete schema.
3. **Mortgage calc default values when research fails.** Reasonable fallback constants the realtor can verify and override.
4. **HTML template line count.** Holden's was ~1,700 lines. We can pre-author the templates as static files and parameter-substitute, or generate dynamically. Static parameter-substitute is simpler.
5. **Voice profile prose injection points.** Which specific sections of the HTML output get voice-styled prose vs which are structural / numeric only? List during implementation.

---

## Success criteria

The skill is working when:

1. Holden can run `/cma` on a real listing appointment scenario and get presentation-ready output in under 10 minutes (including pre-flight + corrections + research + draft).
2. The HTML output passes a self-presentation test — Holden would actually show it to a seller without edits more than 70% of the time on first draft.
3. The output looks visually identical in spirit to the 6333 Blackmar presentation but styled to whatever brand kit is active.
4. Buyer-mode produces 3-tab offer strategy with the scenarios he discusses with the realtor as pre-flight.
5. State-specific math (transfer tax, title insurance, tax uncapping) is correctly researched and cited for any U.S. state, not just Michigan.
6. Post-write feedback loop genuinely supports realtor edits — drop a comp, edit an adjustment, edit a weight, edit a recommendation, all without restarting from scratch.
7. Output file lands at the documented path and opens cleanly in Chrome / Safari / iOS Safari / Android Chrome.

---

## Next step

After approval: write the brand-kit-capture spec (much shorter, mirrors voice-draft), then invoke `writing-plans` to produce implementation plans for both skills.
