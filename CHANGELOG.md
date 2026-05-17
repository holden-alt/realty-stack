# Changelog

All notable changes to Realty Stack are tracked here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [Semantic Versioning](https://semver.org/).

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
