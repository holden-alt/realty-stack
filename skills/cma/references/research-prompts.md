# /cma Skill — Live Research Prompts Reference

Canonical WebSearch / WebFetch query templates for the /cma skill's live research phase.
Use these for every invocation. Do NOT hardcode state-specific values in the skill itself —
research live instead so the skill works in all 50 states on day 1.

**Variable placeholders used throughout:**
- `{state}` — full state name (e.g., "Michigan") or two-letter code where noted
- `{county}` — county name without "County" suffix (e.g., "Kent")
- `{msa}` — metro statistical area name (e.g., "Grand Rapids-Kentwood MSA")
- `{city}` — city or township name (e.g., "Grand Rapids")
- `{district}` — school district name (e.g., "Bridgeport-Spaulding Community Schools")

---

## Topic 1: State Real Estate Transfer Tax Rate

**Why we research this:** Transfer tax is a direct seller cost on the net sheet. Every state has a different
rate, statute, and rounding rule; hardcoding any of them would produce incorrect net sheets for out-of-state CMAs.

**Canonical query template:**
```
"{state} real estate transfer tax rate 2026"
```
Also try if primary returns no result:
- `"{state} SRETT rate"` — useful for Michigan specifically
- `"{state} documentary transfer tax rate"` — used in many western/southern states
- `"{state} deed transfer tax"` — alternative terminology in northeastern states

**Primary sources (in priority order):**
1. State department of treasury official website — authoritative, cites the controlling statute
2. State statutes directly (e.g., MCL 207.502 for Michigan, RCW 82.45 for Washington) — resolves rounding rules
3. State bar association real estate law section — practitioner-verified rates
4. NCSL.org state transfer tax comparison table — broad coverage but may lag by 1–2 years; verify against state site

**Fallback if research inconclusive:** Ask the realtor. They execute closings regularly and know their state's
rate cold. Do not fabricate or use a neighboring state's rate as a proxy.

**Example of a good answer:**
"Michigan SRETT = $3.75 per $500 of consideration (or fraction thereof), rounded UP to the next $500 increment
per MCL 207.502. On a $250,000 sale: $250,000 ÷ $500 = 500 increments × $3.75 = $1,875.00 seller transfer tax."

**Citation format for output:**
```
{State} State Transfer Tax per {statute citation}: ${rate} per $500
```

---

## Topic 2: County Transfer Tax

**Why we research this:** Many states authorize an additional county-level transfer tax on top of the state tax.
Michigan alone has 83 counties each with their own rate. Missing this produces an understated net sheet.

**Canonical query template:**
```
"{county} county {state} real estate transfer tax"
```
Also try:
- `"{state} county transfer tax rates by county"` — often returns a table for all counties
- `"{county} county register of deeds transfer tax"` — direct from the collecting authority

**Primary sources (in priority order):**
1. County treasurer or register of deeds website — authoritative for their jurisdiction
2. State statutes governing county authority to levy (confirms whether counties in this state can levy at all)
3. Local title company rate sheets or closing fee guides — practitioner-verified
4. State association of counties publications — often maintain a statewide rate table

**Fallback if research inconclusive:** Ask the realtor; or default to $0.00 with explicit note
"county transfer tax not confirmed — verify before using." Never assume county tax equals $0
without checking; never assume it mirrors the state rate.

**Example of a good answer:**
"Saginaw County, MI: $0.55 per $500 of consideration per county ordinance. Kent County, MI: $0.55 per $500.
Wayne County, MI: $0.75 per $500 (higher rate authorized by MCL 207.505)."

**Citation format for output:**
```
{County} County Transfer Tax per {statute or county ordinance}: ${rate} per $500
```

---

## Topic 3: State Owner's Title Insurance Rate Schedule

**Why we research this:** Owner's title insurance is a standard seller cost in most states and uses
a graduated tier schedule that varies by state filing. The cost is material on mid- and high-priced properties.

**Canonical query template:**
```
"{state} owner's title insurance rate schedule 2026"
```
Also try:
- `"{state} title insurance basic rate per thousand"` — returns per-$1K tier rates
- `"{state} department of insurance title insurance rate filing"` — the controlling document
- `"{state} title insurance promulgated rates"` — applies in states like Texas where rates are state-mandated

**Primary sources (in priority order):**
1. State insurance commissioner's office or department of insurance — controls the filed rates
2. Major title underwriter rate guides: First American, Fidelity National Title, Old Republic, Stewart Title
3. State bar real estate section's closing cost guide — practitioner-verified
4. ALTA (American Land Title Association) state-by-state resource page

**Fallback if research inconclusive:** Ask the realtor for the local convention; or contact a local title company
for their current rate sheet. Some states (e.g., Iowa) have a unique state fund — the realtor will know.

**Example of a good answer:**
"Michigan graduated owner's title insurance: first $100,000 at $5.75 per $1,000; $100,001–$500,000 at $3.40 per $1,000;
above $500,000 at $2.50 per $1,000. On a $250,000 policy: (100 × $5.75) + (150 × $3.40) = $575 + $510 = $1,085."

**Citation format for output:**
```
{State} Owner's Title Insurance per state filed rates: graduated schedule — ${rate1}/$1K to ${amount1}, ${rate2}/$1K above
```

---

## Topic 4: State Property Tax Reassessment-on-Sale Rules

**Why we research this:** In many states, the buyer's go-forward property tax burden jumps significantly after purchase
because assessed value uncaps or resets to market value. This is a material disclosure the CMA must surface.

**Canonical query template:**
```
"{state} property tax reassessment on sale 2026"
```
Also try:
- `"{state} property tax uncapping on transfer"` — Michigan-specific terminology
- `"{state} Proposition 13 property tax"` — California and states with similar caps
- `"{state} property tax assessment increase after purchase"`
- `"{state} homestead exemption loss on sale"`

**Primary sources (in priority order):**
1. State department of treasury or state revenue authority — defines the controlling rule
2. Local county assessor's office FAQ — often explains the mechanism in plain language
3. State realtor association guidance documents — written for practitioners, cites statutes
4. State legislature's official statutes — resolves edge cases (partial transfers, inherited property, etc.)

**Fallback if research inconclusive:** Ask the realtor. This is local-knowledge territory; the rule materially
affects buyer affordability estimates and must be accurate or omitted entirely — do not guess.

**Example of a good answer:**
"Michigan Proposal A (1994) — taxable value is capped at inflation or 5% annually while a property is owner-occupied.
On transfer (sale), the cap is removed ('uncapped') and taxable value resets to State Equalized Value (50% of market
value) the following tax year. A buyer purchasing a $250,000 home where the seller's taxable value was $95,000 should
expect taxable value to rise toward $125,000, potentially increasing annual taxes by $3,000–$5,000 depending on millage."

**Citation format for output:**
```
{State} property tax {rule name} — {brief mechanism description}; buyer's taxable value resets to {mechanism} on transfer
```

---

## Topic 5: Local Market Appreciation (YoY + Forecast)

**Why we research this:** Time adjustments on comps require a reliable monthly appreciation rate for the
subject's market. Using national averages instead of MSA-specific data introduces systematic error.

**Canonical query template:**
```
"{msa} home price appreciation 2026"
```
Also try:
- `"{msa} median sale price year over year"`
- `"{msa} home value forecast 12 months"`
- `"{city} {state} real estate market trends 2026"`

**Primary sources (in priority order):**
1. Redfin Data Center MSA page — current YoY median sale price change, updated monthly
2. Zillow Home Value Index (ZHVI) and Home Value Forecast for the MSA — 12-month forward forecast
3. FHFA All-Transactions House Price Index (HPI) — quarterly, government-sourced, most defensible for appraisal
4. Local MLS year-to-date statistics — most granular but may require login; ask realtor for access

**Fallback if research inconclusive:** Ask the realtor for their market's current appreciation trend;
or default to national average (~3.6%/year ≈ 0.30%/month) with explicit note "national default used —
verify against local MLS."

**Example of a good answer:**
"Grand Rapids-Kentwood MSA: +4.2% YoY median sale price (Redfin, April 2026), +5.1% 12-month forecast
(Zillow ZHVI, April 2026). Monthly time adjustment rate: ~0.35%/month applied to comp sale price."

**Citation format for output:**
```
{MSA} market appreciation: +{YoY}% YoY per {source} ({month/year}), +{forecast}% forecast per {source} ({month/year})
```

---

## Topic 6: School District Rankings

**Why we research this:** School district is a primary value driver, especially in suburban and family markets.
A subject and a comp in different districts require an explicit quality adjustment. Research each unique district
from both the subject property and every comp.

**Canonical query template:**
```
"{district} {state} school district ranking"
```
Run this query once per unique district across subject + all comps. Do not batch districts into a single query.
Also try:
- `"{district} school district rating GreatSchools"`
- `"{district} school district rank PublicSchoolReview"`
- `"{city} {state} public school district quality ranking"`

**Primary sources (in priority order) — use AT LEAST TWO per district and triangulate:**
1. PublicSchoolReview — provides statewide rank (e.g., "#787 of 851 Michigan districts")
2. GreatSchools — provides 1–10 composite score; most consumer-facing
3. SchoolDigger — star ratings and percentile statewide
4. US News & World Report Best High Schools rankings — useful for secondary school quality

**Fallback if research inconclusive:** Ask the realtor for their local read. School district quality is a
hyperlocal judgment call; a long-tenured local agent's assessment often outperforms aggregate data.

**Example of a good answer:**
"Bridgeport-Spaulding Community Schools (Saginaw County, MI): ranked #787 of 851 Michigan districts
(PublicSchoolReview, 2025), rated 3/10 (GreatSchools, 2025) → bottom-tier classification.
Forest Hills Public Schools (Kent County, MI): ranked #18 of 851 Michigan districts
(PublicSchoolReview, 2025), rated 9/10 (GreatSchools, 2025) → top-tier classification."

**Citation format for output:**
```
{District}: #{rank} of {total} {state} districts (per {source1}, {year}); {score}/10 (per {source2}, {year})
```

---

## Topic 7: Current 30-Year Fixed Mortgage Rate

**BUYER-SIDE ONLY.** Used in the buyer's monthly payment calculator on the CMA.

**Why we research this:** The default mortgage rate in the buyer calculator must reflect current market
conditions. A stale rate produces meaningfully wrong monthly payment estimates and misleads buyers.

**Canonical query template:**
```
"current 30-year fixed mortgage rate 2026"
```
No state placeholder needed — use the national average as the default.
Also try:
- `"Freddie Mac PMMS 30-year fixed rate this week"`
- `"30-year fixed mortgage rate Bankrate today"`

**Primary sources (in priority order):**
1. Freddie Mac Primary Mortgage Market Survey (PMMS) — weekly, government-backed, most authoritative;
   published every Thursday at freddiemac.com/pmms
2. Bankrate national average — daily update, widely cited
3. NerdWallet national mortgage rate tracker — daily update, consumer-facing

**Fallback if research inconclusive:** Default to 6.5% with explicit note:
"Rate as of unknown date — buyer should confirm current rate with their lender."
Never present a defaulted rate without the lender-confirm disclaimer.

**Example of a good answer:**
"30-year fixed national average: 6.875% (Freddie Mac PMMS, week of May 15, 2026).
Monthly P&I on $200,000 loan: ~$1,314."

**Citation format for output:**
```
30-yr fixed mortgage rate: {rate}% per {source}, week of {date}
```

---

## Topic 8: Area Effective Property Tax Rate

**BUYER-SIDE ONLY.** Used to estimate the buyer's monthly property tax escrow.

**Why we research this:** Property tax as a percentage of value varies enormously by county — from under 0.5%
in Hawaii to over 2.5% in parts of New Jersey. A wrong rate here produces a materially incorrect PITI estimate.

**Canonical query template:**
```
"{county} county {state} effective property tax rate"
```
Also try:
- `"{state} property tax rate by county 2026"` — often returns a full county table
- `"{city} {state} property tax rate"` — useful for city-assessed taxes on top of county
- `"SmartAsset {county} county {state} property tax"`

**Primary sources (in priority order):**
1. SmartAsset property tax calculator by county — broad county coverage, annually updated
2. County assessor or treasurer website — authoritative for millage rates; requires manual math
3. Tax Foundation state property tax data — state averages plus county breakdowns where available
4. National Association of Realtors research: "Property Taxes by State" — annual publication

**Fallback if research inconclusive:** Ask the realtor; or default to the statewide effective average
from Tax Foundation with explicit note "statewide average used — confirm county-specific rate."

**Example of a good answer:**
"Kent County, MI effective property tax rate: approximately 1.42% of assessed value (SmartAsset, 2025).
On a $250,000 home assessed at $125,000 (50% SEV in Michigan): $125,000 × 1.42% = ~$1,775/year → ~$148/month escrow."

**Citation format for output:**
```
{County} {State} property tax: ~{rate}% of assessed value per {source} ({year})
```

---

## Topic 9: Area Homeowner's Insurance Estimate

**BUYER-SIDE ONLY.** Used to estimate the buyer's monthly HO insurance escrow.

**Why we research this:** HO insurance costs vary significantly by state and metro — coastal, tornado corridor,
and hail-prone markets run 2–3× the national average. Using a flat national default misleads buyers in high-risk areas.

**Canonical query template:**
```
"average homeowners insurance cost {city} {state} 2026"
```
Also try:
- `"{state} average homeowners insurance annual premium"` — useful when city-level data is unavailable
- `"cheapest homeowners insurance {state}"` — Bankrate/Policygenius guides often embed state averages
- `"home insurance cost estimate {state} Bankrate"`

**Primary sources (in priority order):**
1. Bankrate state homeowners insurance guides — annually updated, city-level data for major metros
2. Insurance.com state insurance cost reports — comparison of average annual premiums by state
3. ValuePenguin homeowners insurance cost analysis — state and metro breakdowns
4. Policygenius annual home insurance pricing report — state averages with high/low ranges

**Fallback if research inconclusive:** Default to $1,500/year with explicit note:
"Estimate only — buyer should obtain actual quotes before budgeting."
Never present the $1,500 default without the confirm-with-quote disclaimer.

**Example of a good answer:**
"Average homeowners insurance Grand Rapids, MI: ~$1,200/year (Bankrate, 2025).
Monthly escrow: ~$100/month."

**Citation format for output:**
```
HO insurance estimate: ~${amount}/year per {source} ({year}) for {city}, {state}
```

---

## Research Phase Orchestration

### When to run research
Run all applicable topics at the start of each /cma invocation, before generating any output.
Topics 1–6 apply to every CMA. Topics 7–9 apply only when generating buyer-side output
(monthly payment calculator, buyer net sheet). Do not skip Topics 7–9 for buyer CMAs —
the payment estimate is a primary consumer of this skill.

### Session-level caching
Within a single /cma session, cache every research result and reuse across comps:
- Topics 1–4 (state/county tax, title, reassessment): same values for every property in the same state/county
- Topic 5 (market appreciation): same value for all comps within the same MSA
- Topic 6 (school districts): cache per unique district name; re-use when multiple comps share the same district
- Topics 7–9 (mortgage rate, property tax, HO insurance): single lookup per session

If the subject and a comp are in different counties, run Topic 2 and Topic 8 separately for each county.
If the subject and a comp are in different school districts, run Topic 6 for each district.

### Citation discipline
Cite EVERY researched number inline in the output at first use. No exceptions.
Format: parenthetical inline citation immediately after the number.
Example: "Kent County transfer tax: $137.50 (Kent County, MI per county ordinance: $0.55/$500)"

Do not cite the same source repeatedly in subsequent uses of the same number — cite once at first
appearance per section, then use the number without repeating the citation.

### Handling inconclusive research
If a WebSearch query returns no clear authoritative answer after two query variants:
1. Flag the specific topic as "not confirmed"
2. Apply the topic's designated fallback (see each topic above — most say "ask the realtor")
3. Note in the output: "[Topic X not confirmed via research — realtor to verify]"
4. Never fabricate a rate, never use a neighboring state's value as a proxy

### Research cache block
At the bottom of every generated HTML output, append a collapsed "Research Cache" section.
Include one row per researched fact:
```
| Topic | Value used | Source | Date retrieved |
|-------|-----------|--------|----------------|
| State transfer tax | $3.75 per $500 | MCL 207.502 | 2026-05-17 |
| Kent County transfer tax | $0.55 per $500 | Kent County Register of Deeds | 2026-05-17 |
| ...   | ...       | ...    | ...            |
```
This block lets the realtor audit every number before presenting to a client.
It also surfaces immediately if any fallback defaults were used (flag those rows with "DEFAULT — verify").

### Query execution order
Run research queries in this sequence to front-load the most critical numbers:
1. Topics 1 + 2 (transfer taxes) — needed for seller net sheet header
2. Topic 3 (title insurance) — needed for seller net sheet
3. Topic 4 (reassessment rules) — needed for buyer disclosure
4. Topic 5 (market appreciation) — needed before time-adjusting any comp
5. Topic 6 (school districts) — query all unique districts before scoring comps
6. Topics 7 + 8 + 9 (buyer-side) — only if generating buyer output; run as a batch

Do not wait for Topic 6 results before starting output generation — school district research
can run in parallel with early sections of the output if the runtime environment supports it.
