---
name: cma
description: This skill should be used when a real estate agent asks to "create a CMA", "run a CMA", "comparative market analysis", "comp this property", "what's a fair offer", "offer strategy for", "listing presentation for", "net sheet for", "should my buyer offer", or "help me prepare for a listing appointment". Forks on buyer vs seller. Produces branded self-contained HTML presentation; live research per invocation.
version: 0.0.1
---

# CMA — Comparative Market Analysis

One skill, two paths. Forks early on buyer vs seller and produces a self-contained branded HTML presentation the realtor downloads, reviews, and presents. The seller path produces a 4-tab listing presentation (Overview, CMA, Net Sheet, Marketing); the buyer path produces a 3-tab offer strategy (Scenarios, Math, Mortgage Calculator). The skill consumes the realtor's voice profile (for prose) and brand kit (for visual styling) via the `using-realty-stack` overlay, so output sounds and looks like the realtor's actual work — not generic AI output.

---

## When this skill runs

Auto-route when the realtor says any of:

- "Create a CMA for [client / address]"
- "Run a CMA on [address]"
- "Comparative market analysis for [address]"
- "Comp [address]" / "Comp this property"
- "Help me prepare for a listing appointment at [address]"
- "What's a fair offer on [address]"
- "Offer strategy for [address]" / "Should my buyer offer X for [address]"
- "Net sheet for [address]"
- "Listing presentation for [address]"

### Path fork — buyer or seller

The first clarification is buyer vs seller. Skip the question when the trigger phrasing is unambiguous:

- "listing presentation for", "listing proposal for", "net sheet for", "help me prepare for a listing appointment" → seller path
- "what should my buyer offer", "offer strategy for", "should my buyer offer", "what's a fair offer" → buyer path
- Generic "CMA" / "comp" / "comparative market analysis" → ask: *"Seller-side listing presentation or buyer-side offer strategy?"*

### Profile + brand kit pre-checks

Before doing any CMA work, verify both pre-requisites are loaded by the overlay:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion, then return to the original `/cma` request. Never produce un-voiced output.
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion, then return to the original `/cma` request. Never produce un-branded output.

If both are missing, run `voice-draft` first (voice underpins every drafted line), then `brand-kit-capture`, then continue.

---

## Onboarding workflow

Work through these eight steps in order. Do not skip steps. Do not write the output file until Step 8.

### Step 1 — Clarify buyer or seller

Skip when the trigger phrasing makes it obvious (see "Path fork" above). Otherwise ask once and lock the path for the rest of the session.

### Step 2 — Pre-flight questions

Ask these in a single message to minimize back-and-forth. The question set differs by path.

**Both paths:**

- **Aggressive or conservative calibration?** Affects three layers consistently: narrative framing (confident vs cautious), comp weighting bias (favor higher-priced/recent vs similar/cheaper), and adjustment-range picks (top vs bottom of each rate range in the methodology). Neutral/middle is the default if the realtor declines to choose.

**Seller-only:** no additional questions beyond the above.

**Buyer-only:**

- **Market situation for this property** — sitting unsold? Just hit market (fresh)? Multiple offers already? Cooling market overall?
- **Buyer constraints** — hard ceiling? Willing to stretch above asking?
- **Aggression tolerance** — max-aggressive to win, or conservative offer (willing to lose if it goes over)?
- **Locally-appropriate offer terms beyond price** — open question, agent enumerates what's standard in their market (escalation clauses, appraisal waivers, seller closing-cost coverage, inspection-period length, etc.). Never pre-suggest these — they are regionally variable.
- **How many scenarios to model and how to frame them** — e.g., "Open with X, max walk-away at Y" vs "Floor / target / stretch."

### Step 3 — Collect inputs

Three input categories. Push back when data is insufficient — never analyze on missing data.

**Subject property.** Ask the realtor to drop the MLS detail PDF (read it via the Read tool's `pages` parameter — supports up to 20 pages per request) OR paste the structured data inline. Required fields: address, city, county, state, year built, GLA above grade, GLA below grade (finished + unfinished), bed count, bath count (full + half), lot acres, construction type, HVAC system, water/sewer, garage configuration, outbuildings, pool, school district, prior SEV / tax history, prior listing history.

**Comparable sales — 3 to 5 comps.** Same data shape as the subject. Behavior:

- **Fewer than 3 comps provided:** push back. *"3 minimum for triangulation. Got 2 more I can look at?"* Do not analyze on insufficient comps.
- **More than 5 comps provided:** auto-select the top 5 by similarity to the subject (closest GLA, most recent sale, same county, same school district where possible). Explain the choice in one line. Realtor can swap during the Step 7 feedback loop.

**Condition ratings — explicit ask, never inferred.** *"Quick 1-10 condition rating for the subject and each comp? 1 = brand new, 10 = teardown."* MLS data does not surface this — the realtor must rate from their own walk-through or comp inspection. Required for the subject AND every comp.

**Corrections cascade — before any analysis.** MLS data is frequently stale. Before the first draft runs, ask the realtor to verify the high-impact fields on the subject and each comp:

- Bath count (the single largest adjustment driver — $7,500 per full bath)
- HVAC system + central AC
- Recent renovations (kitchen, baths, mechanicals)
- Basement/foundation type + finish level
- Any other facts the realtor knows differ from MLS

Lock corrections before adjustment analysis begins. If the realtor refuses ("just use the MLS data"), honor it and flag in caveats: *"Adjustments based on MLS data as-provided. Verify against current property condition before presenting."*

### Step 4 — Live research phase

Run the canonical query templates from `references/research-prompts.md` using WebSearch + WebFetch. Apply session-level caching: same state/county/MSA/district lookups reuse across comps.

**Always research (every CMA):**

- State real estate transfer tax rate (seller-side cost on net sheet) — Topic 1
- County transfer tax (where applicable) — Topic 2
- State owner's title insurance rate schedule (seller-side) — Topic 3
- State property tax reassessment-on-sale rules (always — buyer disclosure even in seller presentations) — Topic 4
- Local market appreciation YoY + 12-month forecast (drives the time adjustment on every comp) — Topic 5
- School district rankings — one query per unique district across subject + all comps; use at least two sources per district and triangulate — Topic 6

**Buyer-side only (additional):**

- Current 30-year fixed mortgage rate (Freddie Mac PMMS preferred) — Topic 7
- Area effective property tax rate (county-level) — Topic 8
- Area homeowner's insurance estimate (city/state) — Topic 9

**Citation discipline.** Cite every researched number inline at first use. Format: parenthetical citation immediately after the number. *"Kent County transfer tax: $137.50 (Kent County, MI per county ordinance: $0.55/$500)."* Do not repeat the citation in subsequent uses within the same section.

**Failure handling.** If two query variants both return inconclusive results on a critical value, ask the realtor directly. *"Couldn't find a definitive answer on [X] — what's standard in [area]?"* Never fabricate. Never use a neighboring state's rate as a proxy. Note in output: *"Per realtor input — verify against current state law."*

**Research cache block.** At the bottom of every generated HTML output, append a collapsed table listing every researched fact with its value, source, and date retrieved. Flag any defaulted-fallback values with "DEFAULT — verify" so the realtor sees them before presenting.

### Step 5 — Run analysis

Load `references/cma-methodology.md` and apply the URAR-aligned Sales Comparison Approach.

1. Run `scripts/adjustment-engine.py` to apply the aggressive/conservative knob consistently across every line item — the knob picks the top, midpoint, or bottom of each rate range from the methodology rate library. Same knob setting drives Layer 1 (rate picks), Layer 2 (weighting bias), and Layer 3 (narrative framing) so all three move together.
2. Calculate each comp's adjusted value: `Comp Sale Price + Sum of All Line Adjustments`. Apply the convention strictly: positive = comp inferior to subject (add to comp's price), negative = comp superior (subtract).
3. Compute the weighted reconciliation per Section 8 of the methodology. Apply net-adjustment reliability gates: >25% net adjustment caps that comp's weight at 10-15%. Weights must sum to 100%.
4. Produce the three final numbers per Section 10: indicated value range (5th–95th percentile of comps), recommended list/offer (knob-influenced), probable sale/acceptance range.

### Step 6 — Build the HTML

**Before generating any HTML:** Load `references/output-style-guide.md` to internalize the design discipline rules (accent is a pigment not a fill; geometric discipline; vague-by-default marketing for seller path; phase-based timeline not week-numbered). These rules govern every visual decision in the generated HTML.

Load the appropriate template and substitute every `{{PLACEHOLDER}}` value. The templates are at `references/html-template-seller.html` (4-tab) and `references/html-template-buyer.html` (3-tab). Both templates document their full placeholder list in the leading HTML comment — substitute exhaustively.

**Brand kit substitution (both paths):**

- `{{BG_COLOR}}`, `{{BG_DEEP_COLOR}}`, `{{INK_COLOR}}`, `{{INK_SOFT_COLOR}}`, `{{RULE_COLOR}}`, `{{ACCENT_COLOR}}`, `{{RED_COLOR}}`, `{{GREEN_COLOR}}` — direct hex substitution from `brand-kit.md` Colors section
- `{{ACCENT_SOFT_COLOR}}` — derive from `{{ACCENT_COLOR}}` by lightening and desaturating (simple lightness shift in HSL space, e.g., +25–30% lightness, –40% saturation). Not a stored value — compute on render.
- `{{GOOGLE_FONTS_LINK}}` — full `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` tag for the brand kit's display + mono fonts with their specified weights
- `{{DISPLAY_FONT}}`, `{{MONO_FONT}}` — bare font family names from the brand kit
- `{{WORDMARK_LEFT}}`, `{{WORDMARK_SEPARATOR}}`, `{{WORDMARK_RIGHT}}` — three wordmark parts from the brand kit (rendered as CSS-styled HTML text, never as an image)

**Asset embedding.** If the brand kit has logo / wordmark mark / headshot files in `~/.config/realty-stack/brand-assets/`, base64-embed them inline in the HTML (`data:image/png;base64,...` for PNG, `data:image/svg+xml;base64,...` for SVG). Never reference asset files by path — breaks self-containment when the file is emailed, hosted, or printed.

**Seller path — template-specific:**

- Load `references/html-template-seller.html`
- Compute net sheet defaults by running `scripts/calc-net-sheet.py` with the researched state/county tax rates + title insurance schedule as inputs. Populate `{{DEFAULT_COMMISSION_PCT}}`, `{{DEFAULT_ADMIN_FEE}}`, `{{DEFAULT_TITLE_FEE}}`, `{{DEFAULT_TAX_PRORATION}}`, `{{DEFAULT_WELL_SEPTIC}}`, `{{DEFAULT_MORTGAGE_PAYOFF}}`, `{{DEFAULT_BUYER_CONCESSIONS}}`, `{{DEFAULT_SALE_PRICE}}` from the result
- Inject the state-specific tax math into `{{STATE_TAX_RATE_PER_500}}`, `{{COUNTY_TAX_RATE_PER_500}}`, `{{TITLE_INSURANCE_FUNCTION_BODY}}` so the interactive net sheet calculates correctly when the seller adjusts inputs in-browser
- Render Tab 4 Marketing pillars as vague-by-default, phase-based prose (no week numbers, no specific vendors, no ad budgets — per `references/output-style-guide.md`)

**Buyer path — template-specific:**

- Load `references/html-template-buyer.html`
- Compute mortgage calc defaults by running `scripts/calc-mortgage.py` with the researched mortgage rate + property tax % + HO insurance estimate as inputs. Populate `{{DEFAULT_PURCHASE_PRICE}}`, `{{DEFAULT_DOWN_PAYMENT_PCT}}`, `{{DEFAULT_LOAN_TERM_YEARS}}`, `{{DEFAULT_INTEREST_RATE}}`, `{{DEFAULT_PROPERTY_TAX_PCT}}`, `{{DEFAULT_HO_INSURANCE}}`, `{{DEFAULT_OTHER_MONTHLY}}` from the result
- Generate `{{SCENARIO_LIST_HTML}}` from the realtor's pre-flight scenario framing (e.g., "Open with X, max walk-away at Y")
- Generate `{{SCENARIO_PRESET_CHIPS_HTML}}` so the buyer can flip between scenarios in the mortgage calc

**Generating SCENARIO_PRESET_CHIPS_HTML (buyer path):** for each scenario from Step 2's pre-flight (e.g., "Recommended", "Aggressive", "Stretch"), output one `<button class="preset-chip" data-preset="<offer_amount>">Label · $<offer_amount>K</button>`. The first/recommended chip gets `class="preset-chip active"`. Example:

```html
<button class="preset-chip active" data-preset="385000">Recommended · $385K</button>
<button class="preset-chip" data-preset="400000">Aggressive · $400K</button>
<button class="preset-chip" data-preset="410000">Stretch · $410K</button>
```

The JS handles click-to-update-purchase-price wiring (already in the template).

**Complex placeholder rendering (both paths):**

- `{{COMP_LIST_HTML}}` — one accordion block per comp containing: header (address + sale price + sale date + adjusted value), full adjustment grid (line item / subject value / comp value / dollar adjustment), comp notes prose. Use the 6333 Blackmar source HTML's comp accordion structure as the canonical pattern.
- `{{RECONCILIATION_TABLE_ROWS}}` — one row per comp with adjusted value, assigned weight, and weighted contribution; totals row at bottom
- `{{WEIGHTING_RATIONALE}}` — Email Voice prose explaining why each comp got its weight; flag any comp that dominates (>35% weight) with explicit reasoning
- `{{CAVEATS_BLOCK}}` — high-net-adjustment flags, MLS-data-only flags (if corrections refused), low-comp-count warnings, time-period bracket notes

**Voice profile consumption.** Use Email Voice (not Text Voice — CMAs are long-form professional documents) for every prose placeholder:

- Seller path prose: `{{LEAD_PARAGRAPH_1}}`, `{{LEAD_PARAGRAPH_2}}`, `{{STRATEGIC_TAKEAWAY}}`, `{{INFO_CARD_LEFT}}`, `{{INFO_CARD_RIGHT}}`, `{{CLOSING_PULLQUOTE}}`, `{{MARKET_CONDITIONS_PARA}}`, `{{WEIGHTING_RATIONALE}}`, `{{CAVEATS_BLOCK}}`, `{{MARKETING_LEAD_PARAGRAPH}}`, `{{MARKETING_PILLARS_HTML}}` (narrative portions), `{{MARKETING_CLOSING_PULLQUOTE}}`
- Buyer path prose: `{{LEAD_PARAGRAPH_1}}`, `{{LEAD_PARAGRAPH_2}}`, `{{NEGOTIATION_READ}}`, `{{OFFER_STRATEGY_CLOSE}}`, `{{MARKET_CONDITIONS_PARA}}`, `{{WEIGHTING_RATIONALE}}`, `{{CAVEATS_BLOCK}}`, scenario rationales inside `{{SCENARIO_LIST_HTML}}`

Pull the realtor's name, brokerage, and primary market from the voice profile's Agent Profile section. Don't ask again.

### Step 7 — Show draft + feedback loop

Do not write the HTML to disk yet. Present a voice summary of the key numbers in chat and offer to download/preview:

- Indicated value range, recommended list/offer, probable sale/acceptance
- One-line comp count + weighting summary
- Any caveats or flags the analysis surfaced (low reliability, refused corrections, defaulted research values)

Then ask: *"Feel right? Anything off? You can:"*

- Drop a comp (re-runs reconciliation)
- Add a new comp (collects data + condition rating, re-runs reconciliation)
- Edit any specific adjustment value (re-runs that comp's adjusted value + reconciliation)
- Edit comp weights manually (re-runs reconciliation)
- Edit the final recommendation directly (keep the math, just update the number + the narrative around it)
- Add a custom disclosure
- Re-run with the aggressive/conservative knob in the other direction

Accept freeform feedback in plain English — the realtor doesn't need to pick from the list. Per round: apply the feedback, regenerate the output, show the updated summary. Loop until approval.

Approval phrases: *"ship it" / "looks good" / "approved" / "good enough" / "save it" / "OK as-is" / "done" / "perfect"* — or any semantic equivalent. Treat as approval and proceed to Step 8.

### Step 8 — Write the file

Only after explicit approval. No partial writes at any earlier point in the workflow.

- **Default output path:** `~/Downloads/<property-slug>-presentation.html`. Slug is the lowercased street address with non-alphanumerics replaced by hyphens (e.g., `1247-plainfield-presentation.html`).
- **Path conflict:** if the default path already exists, append a timestamp suffix: `<slug>-presentation-2026-05-17-1430.html`. Never overwrite an existing file silently.
- **Override:** if the realtor explicitly says *"save to [path]"*, honor it.

Use the Write tool. Confirm the final path back to the realtor in one line: *"Saved to ~/Downloads/1247-plainfield-presentation.html — open in Chrome / Safari to preview, ⌘P prints cleanly with all tabs expanded."*

---

## Voice profile + brand kit consumption

Both files are pre-loaded in context by the `using-realty-stack` overlay. Do not load them directly — read from the overlay-provided context.

**Voice profile (`~/.config/realty-stack/voice-profile.md`).** Use Email Voice for all prose. The Agent Profile section provides the realtor's name (used in signatures and "from your agent" framing), brokerage (used in pullquotes and signature blocks), and primary market (anchors the "Practical & Local" voice tenet — name specific streets and neighborhoods, not generic descriptors). If the file is missing on invocation, run `voice-draft` inline to completion before continuing.

**Brand kit (`~/.config/realty-stack/brand-kit.md`).** Use the eight semantic color roles, the display + mono fonts, the three-part wordmark structure, and any optional asset files (base64-embedded). Derive `{{ACCENT_SOFT_COLOR}}` from the accent color via a lightness + desaturation shift. Treat the accent color as a pigment, never a fill — only the prescribed roles per `references/output-style-guide.md` Section 2 (single character, thin bar, single mono-caption color, single decorative element per panel). If the file is missing on invocation, run `brand-kit-capture` inline to completion before continuing.

---

## Research phase guidance

The full canonical query templates, source priorities, fallback handling, and citation discipline live in `references/research-prompts.md`. Key operating rules:

- **Cite every researched number inline** at first use within each section. Repeat sources within the same section only when ambiguity could result.
- **Session-level cache.** Same state/county/MSA/district = single lookup reused across comps. Different counties or districts on subject vs comp = separate lookups.
- **Inconclusive research** = ask the realtor directly. Never fabricate, never use a neighboring state's value as a proxy.
- **Defaulted fallbacks** (e.g., national mortgage rate, statewide HO insurance average) MUST carry an explicit verify-disclaimer in the output.
- **Research cache block** appended to every generated HTML so the realtor can audit every number before presenting.

---

## Post-write feedback loop knobs

The realtor can adjust any of the following at any point during the Step 7 loop. Each change re-runs the affected portion of the analysis and regenerates the output.

- **Drop a comp** — removes the comp entirely; re-runs reconciliation with remaining comps; updates the indicated range, recommended list/offer, and weighting rationale
- **Add a new comp** — collects the new comp's data + condition rating; runs the full adjustment grid; re-runs reconciliation
- **Edit any specific adjustment value** — replaces a single line item in a single comp's adjustment grid; re-runs that comp's adjusted value; re-runs reconciliation
- **Edit comp weights manually** — bypasses the automatic weighting; the realtor specifies the weights directly (must sum to 100%); re-runs reconciliation; flags the manual override in the weighting rationale
- **Edit the final recommendation directly** — keeps all the comp math intact, just updates the recommended list/offer number and rewrites the surrounding narrative to match the realtor's chosen number
- **Add a custom disclosure** — appends realtor-supplied disclosure text to the caveats block
- **Flip the aggressive/conservative knob** — re-runs the full analysis with the knob in the opposite direction (re-applies adjustment-engine, weighting bias, and narrative framing consistently across all three layers)

---

## Edge cases

| Situation | Behavior |
|---|---|
| Fewer than 3 comps provided | Push back: *"3 minimum for triangulation. Got 2 more I can look at?"* Don't analyze on insufficient data. |
| More than 5 comps provided | Use top 5 by similarity (auto-select), explain choice, realtor can swap during feedback. |
| Condition rating not provided | Always ask explicitly — never infer from MLS data. |
| MLS PDF unreadable / corrupted | Ask for pasted structured data as fallback. |
| Research phase fails for critical state-tax value | Ask realtor directly; cite as *"Per realtor input — verify against current state law."* |
| Realtor refuses corrections cascade | Honor it; flag in caveats: *"Adjustments based on MLS data as-provided. Verify against current property condition before presenting."* |
| Realtor wants to change brand mid-CMA | Out of scope — finish current CMA with current brand; re-run brand-kit-capture for next CMA if needed. |
| Realtor mid-CMA asks unrelated question | Pause gracefully, answer the question, offer to resume the CMA. Do not lose collected state. |
| Output file path already exists | Append timestamp suffix: `<slug>-presentation-2026-05-17-1430.html`. Never overwrite silently. |
| Brand kit missing on invocation | Run `brand-kit-capture` inline to completion, then return to original /cma request. |
| Voice profile missing on invocation | Run `voice-draft` inline to completion, then return to original /cma request. |

---

## What this skill never does

- Auto-send the presentation to clients — output is for the realtor to review and present
- Fabricate market data — always pulls from live web research OR asks the realtor directly
- Skip the corrections cascade — locks facts before the first draft runs so adjustments stay consistent
- Commit to specific vendor names, ad budgets, or weekly milestones in the marketing tab — vague-by-default, phase-based not week-numbered, per `references/output-style-guide.md`
- Pre-suggest regionally-variable offer terms (escalation clauses, appraisal waivers, seller closing-cost coverage) — agent enumerates per their market
- Quietly choose aggressive vs conservative — always asks in pre-flight
- Present any researched number without an inline citation
- Skip the research phase — every invocation runs live research, no cached state-level math from prior sessions
- Hardcode state-specific tax math — every state's transfer tax, title insurance schedule, and reassessment rule is researched per invocation
- Use the accent/brass color as a background fill — it is a pigment, not a fill, per the design discipline

---

✨ Realty Stack v0.0.3 — Realty Brain (FUB-powered always-on AI) coming soon
