# brand-kit-capture — Design Spec

**Status:** Approved 2026-05-17. Ready for implementation plan.
**Author:** Holden Richardson
**Skill:** `skills/brand-kit-capture/`
**Pattern parent:** voice-draft (mirrors its one-time-onboarding-then-persist architecture)
**Required by:** /cma (and every future visual-output skill — listing-flyer, social-card, property-website, etc.)

---

## TL;DR

A one-time onboarding skill that captures the realtor's visual brand kit — colors, typography, wordmark structure, tagline, plus optional logo/headshot asset files — and persists everything to disk so all Realty Stack visual-output skills can produce branded HTML/PDFs without re-asking. Exact same pattern as voice-draft, just for visual brand instead of writing voice.

---

## Motivation

Visual-output skills (CMA presentations, listing flyers, property websites, social cards) need to match each realtor's brand. Asking for brand kit per-skill is friction; hardcoding one brand kills the nationwide bundle thesis.

Voice-draft proved one-time-onboarding-then-persist works. Brand kit is the visual-side equivalent. Build once now, every future visual skill inherits it for free.

---

## Scope

### In scope (v0.0.3)
- One-time onboarding skill that captures the brand kit
- Persists to `~/.config/realty-stack/brand-kit.md` (text) + `~/.config/realty-stack/brand-assets/` (image files)
- Trigger paths: belt + suspenders (SessionStart hook prompt when missing, first-skill-invocation fallback)
- Same refinement loop as voice-draft (freeform feedback + regenerate)
- Overlay loads brand-kit into context every session
- Optional logo + wordmark mark + headshot asset files

### Out of scope (deferred)
- Live brand-kit editing UI
- Multiple brand kits per realtor (e.g., personal brand + brokerage brand) — single kit per device for v0.0.3
- Auto-extraction of brand kit from existing website / business card / etc.
- Style guide enforcement (linting outputs against the brand)

---

## Design

### Skill purpose

Capture the realtor's visual brand kit one time, persist it locally, expose it to every Realty Stack visual-output skill via the overlay.

### Triggers

Two paths (mirrors voice-draft):

**Path A — SessionStart hook (primary).**
When the realtor opens a session and the brand-kit file doesn't exist, the SessionStart hook output includes a prompt offering the brand-kit onboarding alongside or after voice-draft. Both onboardings can run in the same session.

**Path B — First-visual-skill-invocation fallback (belt + suspenders).**
If the realtor invokes `/cma` (or any future visual skill) and the brand kit is missing, the visual skill detects the absence and runs brand-kit-capture inline before completing the original request.

### Triggers (description phrases)

The skill auto-routes when the agent asks to:
- "set up my brand"
- "capture my brand"
- "configure my brand kit"
- "I just installed realty stack" (in conjunction with voice-draft for first-time setup)
- "add my logo"
- "set my brand colors"

### Onboarding workflow

**Step A — Tagline / positioning line (1 field)**
- The agent's wordmark / positioning line (e.g., "Holden/GR — Ambassador To RealSavvy")
- Optional — agent can say "no tagline"

**Step B — Wordmark structure (text-rendered mark)**
Ask the agent to describe their wordmark in three parts:
- Left segment text (e.g., "Holden")
- Separator (e.g., "/" or "·" or "—" or none)
- Right segment text (e.g., "GR")

Wordmark renders as CSS-styled HTML text in outputs — no image dependency. Sharp at any resolution.

**Step C — Brand colors (8 hex values)**
Ask for hex values for:
- `bg` — page background
- `bg-deep` — panels, input areas (typically 5-10% darker than bg)
- `ink` — primary text / strong contrast
- `ink-soft` — body text (typically a muted version of ink)
- `rule` — borders / dividers
- `accent` — the brass-equivalent; used only as accent, never as fill
- `red` — warnings / caveats
- `green` — positive / success

If the agent only has 2-3 colors, suggest tasteful defaults for the rest based on what they provided.

**Step D — Typography (2-3 font choices)**
- Display font (Google Fonts name + weights, e.g., "Inter 400/500/600/700")
- Mono font (Google Fonts name + weights, e.g., "JetBrains Mono 400/500")
- Optional body font (defaults to display font if not specified)

Validate that the font is on Google Fonts before saving (skill does a quick lookup).

**Step E — Optional asset files**
Ask if the agent wants to add:
- **Logo (full)** — drop a file path or paste base64; SVG preferred, PNG fallback
- **Wordmark mark** (icon version) — for favicons, social cards
- **Headshot / agent photo** — for "Why this agent" sections, social syndication

Files copied to `~/.config/realty-stack/brand-assets/<name>.<ext>`. Skill notes path in brand-kit.md.

If agent has no asset files: skip, brand kit works with CSS-rendered wordmark alone.

**Step F — Voice / positioning notes (optional, freeform)**
Anything else about brand positioning that won't show up in voice profile or colors/fonts. Single freeform field. Saved as-is.

**Step G — Confirmation**
Return a single confirmation message:
- Plain-English summary of the captured brand kit
- A small inline preview (HTML rendered as text in chat — colored block samples, wordmark mock)
- Ask: *"Sound right? Or tell me what's off."*

**Step H — Refinement loop**
Freeform feedback in plain English. Agent can:
- Change any color hex value
- Change a font
- Update the wordmark structure
- Add / replace / remove asset files
- Edit the tagline

Loop until agent says approved / done / ship it / save it.

**Step I — Write the brand kit file**
ONLY after approval. Use Bash to ensure `~/.config/realty-stack/` and `~/.config/realty-stack/brand-assets/` exist; use Write to save the brand kit markdown file with the structured content + asset path references.

### Brand kit file format

**Location:** `~/.config/realty-stack/brand-kit.md`

**Format:**

```markdown
# Realty Stack — Brand Kit for [Agent Full Name]
Captured: [ISO date]
Refined: [ISO date] ([N] rounds)

## Wordmark
- Left segment: Holden
- Separator: /
- Right segment: GR
- Render as: HTML/CSS text (no image)

## Tagline
Holden/GR — Ambassador To RealSavvy

## Colors
- bg: #F4F3EF
- bg-deep: #E8E6DF
- ink: #111418
- ink-soft: #3A3F46
- rule: #C7C4BC
- accent: #B08A44
- red: #963c2a
- green: #3d6b3d

## Typography
- display: Inter (weights 400, 500, 600, 700)
- mono: JetBrains Mono (weights 400, 500)
- body: Inter (defaults to display)

## Asset files
- logo: ~/.config/realty-stack/brand-assets/logo.svg
- wordmark mark: (none)
- headshot: ~/.config/realty-stack/brand-assets/holden-headshot.png

## Voice / positioning notes
Brand is geometric/editorial — sharp corners, hairline borders, no shadows, no gradients
except the cover top bar. Brass is a pigment not a fill — single character, thin bar,
or single decorative element. Never as background fill or text emphasis on multiple words.

## Refinement history
- Round 1 (2026-05-17): initial capture from 5 colors + 2 fonts + tagline; added logo SVG + headshot PNG
```

**Format choice rationale:** same as voice profile — Markdown is LLM-friendly to load, human-readable for the realtor to inspect and hand-edit, easy to version and diff.

### Consumption by other skills

The `using-realty-stack` overlay reads `~/.config/realty-stack/brand-kit.md` at session start and injects its contents into context — same loading mechanism as voice-profile.md.

**Asset handling in visual-output skills:** when a skill generates HTML output, it reads the asset files referenced in brand-kit.md from disk and base64-encodes them inline. The HTML output is fully self-contained — works when emailed, hosted, printed.

**Contract:** every Realty Stack visual-output skill must:
1. Assume brand kit is in context (don't re-collect)
2. Use the captured colors for all background / text / border / accent decisions
3. Use the captured typography for all text rendering
4. Embed asset files as base64 in HTML output
5. Fail gracefully if brand kit is missing — run brand-kit-capture inline, then continue with the original request

### Edge cases & failure modes

| Situation | Behavior |
|---|---|
| Agent gives only 2-3 colors of the 8 needed | Skill suggests tasteful defaults for the rest, based on the provided colors. Agent approves or overrides. |
| Agent picks a font that isn't on Google Fonts | Push back: *"That font isn't on Google Fonts — pick a similar one from [list], or paste a CSS @font-face declaration."* |
| Asset file path doesn't exist | Ask for a valid path or skip the asset. |
| Asset file is too large (>500KB for HTML embedding) | Ask agent to provide a smaller version, or warn about HTML file size impact. |
| Onboarding interrupted | Brand kit file isn't written until approval. Next session, SessionStart re-prompts. |
| Brand kit file corrupted | Overlay detects on load, re-triggers onboarding. |
| Agent wants to redo brand later (rebrand) | Realtor manually deletes brand-kit.md, triggers onboarding again. (`/realty-stack:refresh-brand` skill in v0.0.4.) |

---

## Implementation surface

### New
- `skills/brand-kit-capture/SKILL.md` — the workflow
- Update `hooks/scripts/check-voice-profile.sh` → rename to `check-realty-stack-setup.sh`, expand to also check for brand-kit.md and prompt for either/both onboardings if missing
- `docs/specs/2026-05-17-brand-kit-capture-design.md` — this document

### Modified
- `hooks/hooks.json` — point to renamed script
- `skills/using-realty-stack/SKILL.md` — add Step 5: load brand-kit.md if it exists; fallback to inline brand-kit-capture if missing when needed
- `CLAUDE.md` — add a brand-kit contract section (mirrors the voice-profile contract section)
- `CHANGELOG.md` — v0.0.3 entry covers both brand-kit-capture and /cma

### Unchanged
- voice-draft (continues working unchanged)
- All knowledge/ files
- Other repo docs except CLAUDE.md

---

## Success criteria

1. Holden can run brand-kit-capture from a fresh state and have a working brand kit captured in under 5 minutes.
2. Brand kit file at `~/.config/realty-stack/brand-kit.md` is parseable, has all 8 colors, all fonts, the wordmark structure, and either asset file paths OR explicit "no assets" markers.
3. /cma (and any future visual skill) loads brand-kit from overlay context and produces output styled to the captured brand — colors right, fonts right, wordmark rendered.
4. Logo/headshot assets embed correctly as base64 in generated HTML and the HTML works when shared (emailed, hosted, printed).
5. Missing brand-kit triggers inline onboarding when a visual skill is invoked — agent doesn't have to abandon their current request.

---

## Next step

Both this spec and the /cma spec get reviewed by Holden. Once approved, invoke `writing-plans` to produce implementation plans for both skills (likely a combined plan since they're built in the same v0.0.3 cycle and brand-kit-capture is a prerequisite for /cma).
