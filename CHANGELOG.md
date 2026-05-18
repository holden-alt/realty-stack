# Changelog

All notable changes to Realty Stack are tracked here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [Semantic Versioning](https://semver.org/).

## [0.0.5] — 2026-05-18

### Added
- **/buyer-presentation-template skill** — one-time consultative builder for the realtor's reusable buyer-side pitch content (about-me, why-hire-me, buying-process, how-i-find-homes, track-record, testimonials, negotiation-philosophy, buyer-rep-agreement). 8 standard sections mapped to the same 4-tab structure as listing-presentation. Step 0 state scan inherits up to 4 sections from listing-presentation-template if present — realtor only fills the 4 buyer-specific sections. First concrete payoff of the new State scan contract.
- **/buyer-presentation skill** — per-meeting skill that loads the saved buyer template + light personalization (buyer name, target property OR "home search", meeting date, optional custom note) and produces both `.html` (browser preview) and `.pdf` (print/email-ready) via the canonical Artifact output contract. Optional inline `/cma` (buyer path) offer at Step 3 — one meeting, both artifacts.
- **`scripts/render-pdf.sh`** (promoted from skills/listing-presentation/scripts/) — shared headless-Chrome PDF renderer. Used by every visual-output skill per the new Artifact output contract.
- **CLAUDE.md "Artifact output contract"** — canonical rule: every visual-output skill produces BOTH `.html` and `.pdf`. Documents render-pdf.sh usage, graceful Chrome-missing fallback, MUST do / MUST NOT do.
- **CLAUDE.md "State scan contract"** — canonical rule: every intake skill scans existing `~/.config/realty-stack/` state BEFORE asking the realtor for material. Pulls inheritable content from sibling artifacts. The system gets smarter as it accumulates state.

### Changed
- **/cma now produces both `.html` and `.pdf`** by default (seller AND buyer paths). Step 8 invokes the shared `render-pdf.sh`. Closes the asymmetry with /listing-presentation (which got the same treatment in v0.0.4).
- **/listing-presentation-template, /brand-kit-capture, /voice-draft** — each gains a Step 0 state scan per the new State scan contract. Inherits relevant fields/sections from sibling artifacts where they exist (e.g., brand-kit-capture pre-fills agent name from voice profile; voice-draft offers to mine listing-pres template About Me prose as supplemental voice samples).
- **/listing-presentation SKILL.md** — render-pdf.sh path updated to the shared `${CLAUDE_PLUGIN_ROOT}/scripts/render-pdf.sh`.
- **using-realty-stack overlay** — catalog updated v0.0.4 → v0.0.5 with rows for both new buyer-side skills.
- **Funnel hook footer** — synced across all 8 skills to `✨ Realty Stack v0.0.5`.

### Notes
- The two new contracts (Artifact output, State scan) are the architectural backbone for v0.0.5+. Future skills inherit them automatically — every new intake skill scans state before asking; every new visual skill produces HTML+PDF.
- The buyer-presentation pair is the first concrete test of the State scan contract — agents who already built their listing-presentation-template see 4 of 8 sections pre-populated before being asked anything.

## [0.0.4] — 2026-05-17

### Added
- **/listing-presentation-template skill** — one-time consultative builder that captures the realtor's reusable listing-presentation content (about-me, process, marketing philosophy, track record, testimonials, pricing, fees). Hybrid front-loaded data dump → categorize into 8 standard sections → propose structure → fill gaps → draft each section in Email Voice → confirmation → refinement loop → save. Persists to `~/.config/realty-stack/listing-presentation-template.md`. Mirrors voice-draft + brand-kit-capture's one-time-onboarding-then-persist pattern.
- **/listing-presentation skill** — per-listing skill that loads the saved template + light personalization (seller name, property address, appointment date, optional custom note) and produces a self-contained branded 4-tab HTML pitch (Who I Am / How I Work / Track Record / Working Together). Optional inline `/cma` offer at Step 3 — one appointment, both artifacts.
- **Canonical Tab Affordance + Print Compatibility patterns** in `skills/cma/references/output-style-guide.md` §8 (tabs) and §7 (print, expanded). Document the v0.0.4 button-shaped tab pattern (`border-radius: 0` preserves the geometric discipline; affordance comes from `bg-deep` fill + rule border + active ink/bg inversion + brass on active tab-num) and the comprehensive `@media print` block (all tabs expand, page breaks between major sections, interactive controls hidden, brand colors preserved on cover hero, Letter geometry, link URLs stripped).

### Changed
- **/cma seller HTML template (`html-template-seller.html`)** — applies the new Tab Affordance + Print Compatibility blocks. Tab markup gains ARIA roles (`role="tablist"`, `role="tab"`, `aria-selected`). JS toggles `aria-selected` alongside `.active`. Seller-specific print extension preserves `.tab-panel` content widget visibility (net-sheet calc) and force-expands `.comp-accordion` / `.pillar-accordion` content. Mobile `nav.tabs` override gains `flex-wrap: nowrap; overflow-x: auto;` to preserve horizontal-scroll pattern.
- **/cma buyer HTML template (`html-template-buyer.html`)** — same retrofit as seller. 3 tabs (Scenarios / Comparables / Mortgage). Buyer-specific print extension preserves mortgage-calc widgets and `.comp-accordion` expansion.
- **using-realty-stack overlay** — catalog updated from v0.0.3 to v0.0.4 with rows for both new skills.
- **Funnel hook footer** — synced across all skills to `✨ Realty Stack v0.0.4`.

### Notes
- The two new skills consume voice profile (Email Voice) and brand kit (all visual styling) via the `using-realty-stack` overlay — no per-invocation re-asking.
- The Tab Affordance + Print Compatibility patterns in `output-style-guide.md` are now the canonical source for every future visual-output skill in the bundle.
- Browser print (Cmd+P → Save as PDF) is the path for shareable PDFs — no third-party PDF tooling required.

## [0.0.3] — 2026-05-17

### Added
- **brand-kit-capture skill** — one-time onboarding for the realtor's visual brand kit. Captures 8 colors, typography (Google Fonts), wordmark structure, tagline, and optional logo/wordmark/headshot asset files. Persists to `~/.config/realty-stack/brand-kit.md` and `~/.config/realty-stack/brand-assets/`. Mirrors voice-draft's pattern.
- **/cma skill** — produces self-contained branded HTML CMA presentations. Seller mode: 4-tab listing presentation (Overview, CMA, Net Sheet, Marketing). Buyer mode: 3-tab offer strategy (Scenarios, Math, Mortgage Calculator). URAR-aligned methodology with calibrated rate library. Live nationwide research per invocation (no hardcoded state files). Aggressive/conservative knob applies consistently across framing, weighting, and adjustment-range picks. Post-write feedback loop lets the realtor adjust comps/weights/adjustments/recommendation.
- **Brand kit contract documentation** in CLAUDE.md — covers what visual-output skills MUST and MUST NOT do.
- **SessionStart hook** expanded to check for both voice profile AND brand kit; outputs targeted onboarding prompt for whichever (or both) are missing.

### Changed
- `using-realty-stack` overlay loads brand-kit.md alongside voice-profile.md at session start.
- Hook script renamed: `check-voice-profile.sh` → `check-realty-stack-setup.sh`.

### Notes
- Voice profile + brand kit are per-device (no sync). Realty Brain will provide multi-device sync when it ships.
- /cma uses live WebSearch + WebFetch for state-specific tax math, title insurance, market appreciation, school rankings, mortgage rates, area property tax %, and HO insurance estimates. Every researched number is cited inline in the output for verification.

## [0.0.2] — 2026-05-16

### Changed
- **voice-draft is now a one-time onboarding skill** (was: per-invocation paste-samples). Captures email + text voice + basic profile (name, brokerage, market, signoff) and persists to `~/.config/realty-stack/voice-profile.md`. Downstream drafting skills auto-consume via the overlay.

### Added
- `hooks/hooks.json` + `hooks/scripts/check-voice-profile.sh` — SessionStart hook auto-prompts onboarding when voice profile is missing.
- `using-realty-stack` overlay loads voice profile into context at session start.
- `CLAUDE.md`: voice profile contract for future drafting skills.

### Notes
- Voice profile is per-device (no sync in v0.0.x). Realty Brain (paid sibling) will provide multi-device sync when it ships.

## [0.0.1] — 2026-05-16

### Added
- Initial repository scaffold.
- Brand voice + constitution + fair-housing knowledge base.
- `/voice-draft` skill — draft any realtor message in the agent's own voice from past samples.
- Overlay skill (`realty-stack`) that loads at session start.
- `.claude-plugin/` metadata for self-publishing as a marketplace.
- MIT license.
