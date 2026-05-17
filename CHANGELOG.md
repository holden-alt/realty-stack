# Changelog

All notable changes to Realty Stack are tracked here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [Semantic Versioning](https://semver.org/).

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
