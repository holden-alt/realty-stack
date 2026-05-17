# CMA Methodology Reference

Canonical adjustment library, rate table, weighting rules, and reconciliation methodology for the `/cma` skill.

Derived from Holden Richardson's appraiser-style CMA work in Saginaw County / mid-Michigan rural markets. Rates transfer reasonably to similar Midwest markets. Validate locally before each engagement.

---

## 1. Sales Comparison Approach Overview

Apply the **Sales Comparison Approach (URAR-aligned)** — the standard methodology in residential appraisal and the federal appraisal standard for conventional lending. This approach is the most credible framework for MLS-driven CMA work.

**Core principle:** Every comparable is adjusted line-by-line for differences from the subject property, producing an "adjusted value" that represents what that comparable would have sold for if it had been the subject. The adjusted values are then reconciled — weighted by quality of match — into a final opinion of value.

Key operating rules:
- Work from the comparable's actual sale price. All adjustments modify that price.
- Adjust for differences only. Where the subject and comp are equal on a line, no entry is needed.
- Never apply blanket percentage adjustments to the whole sale price. Adjust each line independently.
- The GLA rate is a **marginal** contribution rate, not total replacement cost. Never apply full $/sqft construction cost to square footage differences.
- Bracket the subject where possible — include at least one comp with more GLA and one with less, one with more acreage and one with less.

---

## 2. Adjustment Convention

Apply this sign convention consistently across all line items:

| Situation | Sign | Effect on Comp Price |
|---|---|---|
| Comp is **inferior** to subject on this line | Positive (+) | Add to comp's sale price |
| Comp is **superior** to subject on this line | Negative (−) | Subtract from comp's sale price |
| Comp and subject are equal on this line | Zero / omit | No change |

**Formula:**

```
Adjusted Value = Comp Sale Price + Sum of All Line Adjustments
```

Example: Comp sold for $275,000. Subject has 200 more sqft of GLA (+$10,000) and a finished walkout basement the comp lacks (+$14,000), but the comp has an extra full bath (−$7,500). Net adjustment = +$16,500. Adjusted value = $291,500.

---

## 3. Adjustment Line Items

Calculate and display each of the following lines for every comparable. Omit only lines where the difference is genuinely zero.

| Line | Description |
|---|---|
| Time / Market Conditions | Months between sale date and current date × monthly appreciation rate |
| School District | Premium or discount based on district ranking (see Section 6) |
| Acreage | Excess acres over 5-acre baseline × per-acre rate (see Section 5) |
| Effective Age | Subject age vs comp effective age; renovated comps carry a lower effective age |
| Condition | Condition rating difference × per-grade rate |
| GLA (above grade) | Square footage difference × per-sqft rate |
| Below Grade | Finished vs unfinished basement; walkout status; square footage |
| Bedrooms | Count difference × per-bedroom rate, measured above a 3 BR baseline |
| Full Baths | Count difference × per-full-bath rate |
| Half Baths | Count difference × per-half-bath rate |
| Garage | Stall count difference + attached vs detached premium + heated/finished premium |
| HVAC | Heat system type + fuel source + cooling type differential |
| Fireplaces | Count difference + type (wood-burning vs gas insert) |
| Kitchen | Recent renovation status; adjust when comp has a dated kitchen vs updated subject |
| Pool / Spa | Inground vs above-ground; saltwater; fenced enclosure |
| Outbuildings | Count, square footage, electric service (pole barn, machine shed) |
| Recreational Features | Trails, hunting cabin, tree stands, food plots |
| Waterfront | Pond, dock, frontage type |
| Construction Quality | 2×6 framing, poured walls, ICF, premium structural features |
| In-Law Suite | Separate kitchen + bath within the dwelling |
| Other Specials | Anything subject-specific not covered by the lines above |

---

## 4. Adjustment Rate Library

These are Holden's calibrated rates for rural and semi-rural Michigan markets, derived from actual appraisal and MLS transaction work.

| Item | Rate | Notes |
|---|---|---|
| GLA above grade | $50/sqft | Marginal cost, not total — never use full $/sqft |
| Finished walkout basement | $35/sqft | Quality matters — heated floors, full bath = top of range |
| Finished standard basement | $25–30/sqft | |
| Unfinished basement | $10/sqft | Storage/utility value |
| Bedroom | $3,000 | Above 3 BR baseline |
| Full bath | $7,500 | High-impact line item |
| Half bath | $3,000 | |
| Garage stall | $5,000 | Attached premium over detached; +$2K for heated |
| Condition grade | $7,500 | Per 1-point on a 10-point scale |
| Effective age | $1,000/year | Capped at ±$25,000 |
| HVAC — full upgrade | $10,000–$15,000 | Wood/window AC vs forced-air natural gas/central |
| HVAC — fuel differential | $3,000–$5,000 | Propane vs natural gas |
| Fireplace | $3,000–$4,000 each | Diminishing returns over 1; second fireplace = bottom of range |
| Inground pool (saltwater) | $20,000 | Net of maintenance perception; above-ground = $0–$3,000 |
| Pole barn 30×50 w/ electric | $30,000–$35,000 | ~$20–25/sqft |
| Pole barn 30×40 | $20,000–$25,000 | |
| Hunting cabin / blind | $5,000–$10,000 | Niche premium; higher end for finished cabin with heat |
| Trail system on acreage | $10,000 | Recreational premium |
| 2×6 + poured walls | $3,000–$5,000 | Build quality premium |
| Waterfront w/ dock + boat | $10,000–$15,000 | Above static pond; frontage and water quality matter |
| In-law suite (kitchen + bath) | $15,000 | Full second living unit within the dwelling |
| Kitchen — recent renovation | $5,000–$10,000 | Apply when comp has dated kitchen vs updated subject |

**Rate range usage:** Where a range is given, the aggressive knob picks the top of the range (favorable to subject's price); the conservative knob picks the bottom; the middle/neutral setting picks the midpoint. See Section 9.

---

## 5. Site / Acreage Adjustment Rate

Apply acreage adjustments above a **5-acre baseline**. Properties with 5 acres or fewer receive no acreage adjustment unless the comp has significantly more land. Excess acres beyond the 5-acre baseline are adjusted at the per-acre rate.

| Scenario | Rate |
|---|---|
| Mid-MI wooded 10-acre parcels | $3,500–$5,830/acre |
| 20-acre parcels | $3,500–$6,000/acre |
| State farm real estate avg (MI) | $6,800/acre |
| Default for wooded recreational | **$4,000/acre** over 5-acre baseline |

Use $4,000/acre as the working default for excess acreage in mid-Michigan recreational/rural markets.

Adjust the rate upward when:
- Land carries mature hardwoods
- Property has waterfront or creek frontage
- Trails, food plots, or hunting infrastructure are developed

Adjust the rate downward when:
- Land is open field or scrub without timber value
- Parcel is oddly shaped or has limited access
- County soil data indicates low productivity or drainage issues

When comps are on dramatically different acreage (e.g., subject is 40 acres, comp is 3 acres), disclose the limitation in the comp notes — the acreage adjustment gets large and reliability drops.

---

## 6. School District Adjustment Tier Table

The school district adjustment is often the single largest non-physical adjustment in rural Michigan markets. Pull current rankings from at least two of:
- PublicSchoolReview
- SchoolDigger
- GreatSchools
- US News & World Report

Map each comp's district against the subject's district. Apply adjustments to the comp based on the tier relationship.

| Tier | Ranking Position | Typical Adjustment to Comp |
|---|---|---|
| Premium district (top 10–20%) | Top decile | −$25,000 to −$40,000 |
| Above-average district | Top 30–40% | −$10,000 to −$20,000 |
| Comparable district | Same general tier as subject | $0 to ±$5,000 |
| Below-average district | Bottom 30–40% | +$10,000 to +$20,000 |
| Bottom-tier district | Bottom decile | +$25,000 to +$40,000 |

Sign logic: if the comp is in a premium district and the subject is in an average district, the comp's location is superior, so the adjustment is negative (subtract from comp's price). If the comp is in a weaker district, add to the comp's price.

Document the source and date of rankings used. Rankings shift yearly.

---

## 7. Market Conditions / Time Adjustment

Derive a monthly appreciation rate from current local market data. Do not rely on stale national figures. Research at least two of:

- Local MSA Redfin or Zillow data — YoY median sale price change
- Zillow Home Value Forecast — forward-looking 12-month projection
- FHFA All-Transactions House Price Index — quarterly, available by MSA
- Local MLS year-to-date stats — average or median sale price change from same period prior year

**Mid-Michigan default (current cycle):** ~0.30%/month (3.6% annualized). Use this as the fallback when live data is unavailable or ambiguous.

**Calculation:**

```
Time Adjustment = Comp Sale Price × (Monthly Rate × Months Since Sale)
```

Apply per comp individually based on its sale date. A comp that sold 18 months ago gets a larger time adjustment than one that sold 3 months ago.

Cap the time adjustment at 36 months. If a comp is older than 3 years, flag it as a weak comparable in the notes and down-weight it accordingly.

When the local market has shifted direction (appreciation to depreciation or vice versa), split the time period at the inflection point and apply different rates for each segment.

---

## 8. Weighting Reconciliation

After computing adjusted values for all comps, assign weights based on quality of match to the subject. Weights must sum to 100%.

| Comp Quality | Weight Range |
|---|---|
| Best GLA match + recent + same county | 25–30% |
| Most recent sale in market area | 25–30% |
| Acreage match but smaller home | 10–15% |
| Distant or dissimilar but bracketing | 10–15% |
| High gross adjustment (>30%) | 5–10% |

**Net adjustment reliability guidelines:**

| Net Adjustment Level | Reliability | Action |
|---|---|---|
| <15% of comp's sale price | High | Full weight as assigned |
| 15–25% of comp's sale price | Moderate | Note in rationale; consider mild downweighting |
| >25% of comp's sale price | Low | Note in rationale; limit to 10–15% max weight |

**Calculation:**

```
Reconciled Value = Sum of (Each Comp's Adjusted Value × Its Weight)
```

Document the weighting rationale in the report narrative. If any single comp dominates the reconciliation (>35% weight), explain why.

When fewer than 3 comps are available, note the limitation explicitly and widen the indicated value range.

---

## 9. Aggressive vs Conservative Knob

The `/cma` skill accepts an `--aggressive` or `--conservative` flag (default: neutral/middle). The knob shifts the analysis across three layers simultaneously.

### Layer 1 — Rate Range Picks

When an adjustment item has a range (e.g., $5,000–$10,000):

| Knob Setting | Rate Used |
|---|---|
| Aggressive | Top of range (maximizes subject's indicated value) |
| Neutral | Midpoint of range |
| Conservative | Bottom of range (minimizes indicated value) |

### Layer 2 — Weighting Bias

Within each comp's quality tier, the knob shifts the actual weight assigned:

| Knob Setting | Weighting Behavior |
|---|---|
| Aggressive | Weight higher-priced comps and the most recent comp more heavily |
| Neutral | Balance weights across quality tiers per the table |
| Conservative | Weight similar-sized and lower-priced comps more heavily; penalize outliers |

### Layer 3 — Narrative Framing

| Knob Setting | Tone |
|---|---|
| Aggressive | Confident — "the comps strongly support pricing at the upper end of the range" |
| Neutral | Balanced — "the comps indicate a value range of X to Y, with the reconciled midpoint at Z" |
| Conservative | Cautious — "the comps suggest care around pricing; the market does not strongly support the top of range" |

The knob does not change which comps are selected or whether adjustments are applied. It only moves the needle within the range of reasonable professional judgment.

---

## 10. Final Opinion of Value

Present three numbers in every CMA output.

### Indicated Value Range

Compute the 5th percentile and 95th percentile of all comp adjusted values. This is the bracketing range — the spread the comps produce before weighting.

### Recommended List Price (Seller) / Recommended Offer (Buyer)

For seller CMAs:
- Aggressive: Recommended list = Reconciled value + 3–5% (negotiation room)
- Neutral: Recommended list = Reconciled value + 2–3%
- Conservative: Recommended list = At or slightly below reconciled value

For buyer CMAs:
- Aggressive: Recommended offer = At or slightly above reconciled value
- Neutral: Recommended offer = Reconciled value
- Conservative: Recommended offer = 3–5% below reconciled value

### Probable Sale Price (Seller) / Probable Acceptance Price (Buyer)

The realistic transaction expectation — what the property will likely actually sell for given current market absorption, list-to-sale ratios, and competitive inventory. Typically lands 1–3% below the recommended list price in a neutral market.

Document all three numbers clearly with the knob setting used. If the knob is neutral, omit the knob notation.

---

## 11. Mandatory Disclosures

Include all three disclosures in every CMA output, regardless of property type or location. Tailor Section 11.1 for non-Michigan properties.

### 11.1 Tax Uncapping / Reassessment on Sale

**Michigan (Proposal A):** When a property transfers ownership, the taxable value uncaps from its capped level to the current State Equalized Value (SEV). The buyer's first-year tax bill may increase significantly over what the seller currently pays — often $4,000–$5,000/year on a $300K property where the seller has been capped for many years.

Disclose this early in the presentation to prevent late-stage deal collapse. Show the buyer the estimated new tax figure, not the seller's current tax.

**For non-Michigan states:** Research the applicable reassessment rule at the time of the CMA. Note it explicitly (e.g., California Prop 13, Florida Save Our Homes, etc.) — this is state-specific and cannot be assumed.

### 11.2 Basement / Foundation Verification

MLS data frequently contains errors or ambiguities about foundation type, basement finish level, and below-grade square footage. The assessor's record card is the more reliable source.

Recommend pulling the assessor's record card before finalizing any listing or offer price. Note in the report if MLS data and assessor data were not cross-checked.

### 11.3 Prior Listing History Lookback

If the subject property was listed previously, include in the report:
- Prior list price
- Days on market (DOM)
- Status change (expired, withdrawn, back on market)
- Whether the current agent confirmed improvements made since that listing

The property as it exists today is not necessarily the property that expired or was withdrawn previously. If improvements have been made, document them explicitly. If no improvements were made and the property failed to sell, the prior DOM and price are evidence — address them directly.

---

*End of CMA Methodology Reference. Load this file at the start of every `/cma` invocation.*
