---
name: brand-kit-capture
description: This skill should be used when a real estate agent asks to "set up my brand", "capture my brand", "configure my brand kit", "I just installed realty stack", "add my logo", "set my brand colors", or when a visual-output skill (like /cma) detects a missing brand kit and needs to onboard the agent inline. One-time onboarding that captures colors, typography, wordmark structure, tagline, and optional logo/headshot assets; persists to ~/.config/realty-stack/brand-kit.md.
version: 0.0.1
---

# Brand Kit Capture

One-time onboarding skill that captures the realtor's visual brand — colors, typography, wordmark structure, tagline, and optional asset files — and persists the result to disk. From that point forward, every Realty Stack visual-output skill auto-uses the captured brand kit so the realtor never re-answers brand questions. Mirrors voice-draft's one-time-onboarding-then-persist architecture for the visual side of the bundle.

---

## When this skill runs

Two trigger paths:

**Path A — SessionStart hook (primary).** When the realtor opens a session and `~/.config/realty-stack/brand-kit.md` is missing, the plugin's SessionStart hook output includes an onboarding prompt offering brand-kit capture alongside or after voice-draft. If the realtor says yes (or any natural affirmation), activate this skill immediately. If they say "later," respect it — but note that any visual-output skill invoked later will trigger brand-kit-capture inline before completing the original request.

**Path B — First-visual-skill-invocation fallback (belt + suspenders).** If the realtor invokes `/cma` (or any future visual-output skill) and the brand kit is missing, that skill detects the absence and runs brand-kit-capture inline to completion before continuing with the original request.

---

## Onboarding workflow

Work through steps A through I in order. Do not skip steps or proceed without sufficient input.

### Step A — Tagline / positioning (1 field, optional)

Ask for the agent's single-line positioning tagline, e.g., *"Holden/GR — Ambassador To RealSavvy"*.

Offer to skip: the agent can say "no tagline" to omit this field entirely. If skipped, record `(none)` in the brand kit file.

### Step B — Wordmark structure (3 parts)

Ask the agent to describe their wordmark in three parts:

1. **Left segment** — e.g., "Holden"
2. **Separator** — e.g., "/" or "·" or "—" or none
3. **Right segment** — e.g., "GR"

Wordmark renders as CSS-styled HTML text in all visual-output skill outputs — no image dependency, sharp at any resolution.

### Step C — Brand colors (8 hex values)

Ask for hex values for each of the following semantic color roles:

| Role | Purpose |
|---|---|
| `bg` | Page background |
| `bg-deep` | Panels, input areas |
| `ink` | Primary text / strong contrast |
| `ink-soft` | Body text (muted) |
| `rule` | Borders and dividers |
| `accent` | Brass-equivalent; used as accent only, never as fill |
| `red` | Warnings and caveats |
| `green` | Positive / success |

If the agent provides only 2-3 colors, suggest tasteful defaults for the remainder using the derivation formulas documented in "Default suggestions when agent provides incomplete data." Show the derived defaults and ask the agent to approve or override before proceeding.

### Step D — Typography (2-3 fonts)

Ask for:

1. **Display font** — Google Fonts name + weights, e.g., "Inter 400/500/600/700"
2. **Mono font** — Google Fonts name + weights, e.g., "JetBrains Mono 400/500"
3. **Body font** (optional) — defaults to display font if omitted

**Validate each font on Google Fonts before saving.** Use WebFetch or WebSearch to confirm the font exists at `fonts.google.com`. If a font is not found on Google Fonts, push back:

> *"That font isn't on Google Fonts — pick a similar one (like [suggest 2-3 similar options]), or paste a CSS @font-face declaration and I'll save it verbatim."*

Do not proceed to Step E until all provided font names pass validation.

### Step E — Optional asset files

Ask: *"Want to add a logo, wordmark mark icon, or headshot? Drop file paths or say skip."*

For each file path provided, handle as follows:

- **Logo (full)** — SVG preferred, PNG fallback. Copy to `~/.config/realty-stack/brand-assets/logo.<ext>` using Bash `cp`. Record the destination path in brand-kit.md.
- **Wordmark mark (icon version)** — for favicons, social cards. Copy to `~/.config/realty-stack/brand-assets/wordmark-mark.<ext>`.
- **Headshot / agent photo** — for "Why this agent" sections. Copy to `~/.config/realty-stack/brand-assets/headshot.<ext>`.

If the provided file path does not exist, ask for a valid path or offer to skip that asset.

If any file exceeds 500KB, warn before copying:

> *"That's a large file — embedding as base64 in HTML outputs will significantly inflate file size. Got a smaller version?"*

Agent can proceed anyway or provide a smaller file. If no asset files are provided, skip — brand kit works with CSS-rendered wordmark alone.

### Step F — Voice / positioning notes (optional, freeform)

Ask: *"Any brand discipline notes that don't fit the fields above? (Or skip.)"*

Single freeform field saved verbatim. Example: *"Brass is a pigment not a fill — single character, thin bar, or single decorative element only."*

### Step G — Confirmation

Return a single response containing all three of the following:

1. **Plain-English summary** (~150 words) of everything captured — wordmark, tagline, all 8 colors with roles, all fonts, any asset files, any positioning notes.

2. **Inline preview:**
   - Colors: list each role + hex clearly (e.g., `bg: #F4F3EF`, `accent: #B08A44`), with a plain-text label of what derived values were suggested if any
   - Wordmark: render as plain text showing the structure (e.g., `Holden / GR` — noting which separator is accent-colored in outputs)

3. Close with: *"Sound right? Or tell me what's off."*

### Step H — Refinement loop

Accept freeform feedback in plain English. Per round:

1. Apply the feedback — change a color, swap a font, edit the wordmark, add / replace / remove an asset, edit the tagline, or update positioning notes
2. Regenerate the inline preview
3. Show the updated summary (~150 words)
4. Ask: *"Better? Or still needs work?"*

Loop until the agent says any of: approved / done / ship it / save it / OK as-is / good enough / looks good — or any semantic equivalent. Treat as approval and proceed to Step I.

### Step I — Write the brand kit file

Write the file ONLY after the agent approves the refinement — never before. No partial writes at any point in the workflow.

1. Use Bash to ensure directories exist:
   ```bash
   mkdir -p ~/.config/realty-stack/ ~/.config/realty-stack/brand-assets/
   ```

2. Confirm any asset files have already been copied to `brand-assets/` (done in Step E). If any copy was deferred, run it now.

3. Use the Write tool to save `~/.config/realty-stack/brand-kit.md` using the file format specified in "Brand kit file format" below.

4. Confirm success:
   > *"Brand kit saved. Every Realty Stack visual-output skill (like /cma) will now use these colors, fonts, and assets automatically."*

---

## Brand kit file format

Write the file to `~/.config/realty-stack/brand-kit.md` using this exact structure:

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

Agent's actual name is pulled from the voice profile already loaded in context by the overlay — do not ask for it again.

---

## Default suggestions when agent provides incomplete data

When the agent provides fewer than 8 color values, derive the missing ones as follows:

| Missing role | Derivation |
|---|---|
| `bg-deep` | Derive from `bg` by darkening 5-10% (reduce lightness in HSL) |
| `ink-soft` | Derive from `ink` by lightening 20-30% (increase lightness in HSL) |
| `rule` | Choose a neutral value roughly halfway between `bg` and `ink-soft` in perceived lightness |
| `red` | Default `#963c2a` if not provided |
| `green` | Default `#3d6b3d` if not provided |
| `accent` | Cannot be derived — must ask the agent; it defines the brand's signature color |

When suggesting derived values, show the hex alongside a plain-English rationale (e.g., *"bg-deep: #E8E6DF — bg darkened ~7%"*). Always surface derivations in the Step G confirmation so the agent can override before approval.

---

## Edge cases

| Situation | Behavior |
|---|---|
| Agent provides only 2-3 colors of the 8 | Suggest tasteful defaults per the derivation formulas above; show them in Step G; agent approves or overrides |
| Agent picks a font not on Google Fonts | Push back; suggest 2-3 similar Google Font alternatives; offer @font-face paste fallback |
| Asset file path doesn't exist | Ask for valid path or offer to skip that asset |
| Asset file >500KB | Warn about HTML inflation; ask for a smaller version; proceed only if agent confirms |
| Onboarding interrupted | File not written until approval — next session re-prompts via SessionStart hook |
| Brand kit file corrupted | Overlay detects on load, re-triggers onboarding with: *"Looks like your brand kit got corrupted — let's redo it."* |
| Agent wants to rebrand later | Manual delete of `~/.config/realty-stack/brand-kit.md` re-triggers onboarding; `/realty-stack:refresh-brand` skill landing in v0.0.4 |
| Mid-onboarding unrelated question | Pause gracefully, answer the question, offer to resume: *"Want to pick back up where we left off on brand onboarding?"* |

---

## What this skill never does

- Auto-save before agent approval — no partial writes, ever
- Fabricate brand assets — all files must be provided by the agent
- Skip the Google Fonts validation for any provided font name
- Overwrite an existing `~/.config/realty-stack/brand-kit.md` without going through a full new onboarding flow
- Reference asset files by path in HTML output — downstream visual-output skills base64-embed the files when generating HTML; the path in brand-kit.md is for loading, not for src= attributes

---

✨ Realty Stack v0.0.3 — Realty Brain (FUB-powered always-on AI) coming soon
