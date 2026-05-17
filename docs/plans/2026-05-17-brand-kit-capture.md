# brand-kit-capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-time onboarding skill that captures the realtor's visual brand kit (colors, fonts, wordmark, tagline, optional logo/headshot assets) and persists to `~/.config/realty-stack/brand-kit.md` + `~/.config/realty-stack/brand-assets/` so all Realty Stack visual-output skills inherit branding without re-asking.

**Architecture:** Mirrors voice-draft's pattern entirely — one-time onboarding, SessionStart-hook-triggered, file-persisted, overlay-loaded into context. The existing SessionStart hook script gets expanded to check for BOTH voice-profile and brand-kit; if either is missing, it prompts for the relevant onboarding.

**Tech Stack:** Markdown (SKILL.md, brand-kit.md), JSON (hooks.json — unchanged structure), Bash (hook script expansion). Same primitives as voice-draft.

**Spec:** `docs/specs/2026-05-17-brand-kit-capture-design.md`

**Prerequisite for:** /cma (and every future visual-output skill)

---

## File Structure

### To Create
- `skills/brand-kit-capture/SKILL.md` — the onboarding workflow

### To Modify (Rename + expand)
- `hooks/scripts/check-voice-profile.sh` → rename to `check-realty-stack-setup.sh`, expand to check both voice profile AND brand kit
- `hooks/hooks.json` — update command path to renamed script

### To Modify (additive)
- `skills/using-realty-stack/SKILL.md` — add brand-kit loading step (similar to existing voice-profile step)
- `CLAUDE.md` — add "Brand kit contract" section (mirrors "Voice profile contract")

### Unchanged
- voice-draft skill
- All knowledge/ files
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- All other docs (README, ETHOS, CONTRIBUTING, SECURITY, etc. — these get touched in the CMA plan when we bump VERSION)

---

## Task 0: Rename + expand the SessionStart hook script

**Files:**
- Rename: `hooks/scripts/check-voice-profile.sh` → `hooks/scripts/check-realty-stack-setup.sh`
- Modify: `hooks/hooks.json` (one-line command path update)

- [ ] **Step 1: Rename the script via git**

```bash
cd ~/Claude/holden-alt/realty-stack
git mv hooks/scripts/check-voice-profile.sh hooks/scripts/check-realty-stack-setup.sh
```

- [ ] **Step 2: Rewrite the script body to check both files**

Write `hooks/scripts/check-realty-stack-setup.sh`:

```bash
#!/usr/bin/env bash
# Realty Stack — SessionStart hook
# Checks for the realtor's voice profile AND brand kit; if either is missing,
# outputs onboarding instructions that Claude will see as additional session context.

set -euo pipefail

VOICE_PROFILE="${HOME}/.config/realty-stack/voice-profile.md"
BRAND_KIT="${HOME}/.config/realty-stack/brand-kit.md"

voice_missing=false
brand_missing=false

[[ ! -f "${VOICE_PROFILE}" ]] && voice_missing=true
[[ ! -f "${BRAND_KIT}" ]] && brand_missing=true

if [[ "${voice_missing}" == true ]] && [[ "${brand_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: voice profile AND brand kit not found]

The user has installed Realty Stack but hasn't completed onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Two quick one-time setups before you use any skills:
> capturing your writing voice (~5 min) and your visual brand kit (~5 min).
> Want to do both now, just one, or skip for now?"

If they say yes to voice → invoke the voice-draft skill.
If they say yes to brand → invoke the brand-kit-capture skill.
If they want both → run voice-draft first, then brand-kit-capture.

If they decline, respect that and answer their actual question. Any drafting
skill (voice-draft consumer) or visual-output skill (brand-kit consumer) they
invoke later will trigger the relevant onboarding inline.
EOF
elif [[ "${voice_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: voice profile not found]

The user has Realty Stack installed but hasn't completed voice onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Voice profile isn't set up yet — about 5 minutes
> one-time. Want to do it now?"

If they say yes → invoke the voice-draft skill.
If they decline, respect that. Drafting skills invoked later will trigger
voice-draft inline.
EOF
elif [[ "${brand_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: brand kit not found]

The user has Realty Stack installed and voice profile captured but brand kit
isn't set up yet. Before responding to their first substantive message, greet
them with:

> "Realty Stack is loaded. Brand kit isn't set up yet — about 5 minutes
> one-time. Want to do it now? (Required before /cma or other visual-output
> skills.)"

If they say yes → invoke the brand-kit-capture skill.
If they decline, respect that. Visual-output skills invoked later will trigger
brand-kit-capture inline.
EOF
fi

exit 0
```

- [ ] **Step 3: Make sure it's still executable**

```bash
chmod +x ~/Claude/holden-alt/realty-stack/hooks/scripts/check-realty-stack-setup.sh
```

- [ ] **Step 4: Update hooks.json to point to renamed script**

Edit `hooks/hooks.json` — change the `command` field from `check-voice-profile.sh` to `check-realty-stack-setup.sh`. The rest of hooks.json structure is unchanged.

The complete new hooks.json:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-realty-stack-setup.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 5: Test all three branches**

```bash
# Test 1: Both files present → silent
mkdir -p ~/.config/realty-stack
touch ~/.config/realty-stack/voice-profile.md ~/.config/realty-stack/brand-kit.md
bash ~/Claude/holden-alt/realty-stack/hooks/scripts/check-realty-stack-setup.sh
# Expected: NO output
echo "Exit: $?"

# Test 2: Brand kit missing only → brand prompt
rm ~/.config/realty-stack/brand-kit.md
bash ~/Claude/holden-alt/realty-stack/hooks/scripts/check-realty-stack-setup.sh
# Expected: "[Realty Stack: brand kit not found]" block

# Test 3: Voice profile missing only → voice prompt  
touch ~/.config/realty-stack/brand-kit.md
rm ~/.config/realty-stack/voice-profile.md
bash ~/Claude/holden-alt/realty-stack/hooks/scripts/check-realty-stack-setup.sh
# Expected: "[Realty Stack: voice profile not found]" block

# Test 4: Both missing → combined prompt
rm ~/.config/realty-stack/brand-kit.md
bash ~/Claude/holden-alt/realty-stack/hooks/scripts/check-realty-stack-setup.sh
# Expected: "[Realty Stack: voice profile AND brand kit not found]" block

# Cleanup
rm -f ~/.config/realty-stack/voice-profile.md ~/.config/realty-stack/brand-kit.md
```

If Holden's actual voice profile exists, restore it after testing: he already has one at `~/.config/realty-stack/voice-profile.md` from the v0.0.2 onboarding.

- [ ] **Step 6: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 7: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add hooks/scripts/check-realty-stack-setup.sh hooks/hooks.json
git commit -m "$(cat <<'EOF'
feat(hooks): expand SessionStart script to check both voice profile + brand kit

Renames check-voice-profile.sh to check-realty-stack-setup.sh and adds
brand kit detection. Outputs targeted onboarding prompts based on which
files are missing (voice only, brand only, both, or neither). Sets up the
infrastructure for brand-kit-capture skill (coming in next task).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 1: Write skills/brand-kit-capture/SKILL.md

**Files:**
- Create: `skills/brand-kit-capture/SKILL.md`

**Spec reference:** `docs/specs/2026-05-17-brand-kit-capture-design.md` Step A through Step I.

**Requirements (all MUST be present):**

1. **Frontmatter:**
```yaml
---
name: brand-kit-capture
description: This skill should be used when a real estate agent asks to "set up my brand", "capture my brand", "configure my brand kit", "I just installed realty stack", "add my logo", "set my brand colors", or when a visual-output skill (like /cma) detects a missing brand kit and needs to onboard the agent inline. One-time onboarding that captures colors, typography, wordmark structure, tagline, and optional logo/headshot assets; persists to ~/.config/realty-stack/brand-kit.md.
version: 0.0.1
---
```

2. **Body sections (in order):**
- **H1:** "Brand Kit Capture"
- Brief intro (≤3 sentences): one-time onboarding, visual brand for all Realty Stack visual-output skills
- **"When this skill runs"** — both trigger paths (SessionStart hook prompt + first-visual-skill-invocation fallback)
- **"Onboarding workflow"** — Steps A through I per the spec:
  - A: Tagline / positioning (1 field, optional)
  - B: Wordmark structure (left segment + separator + right segment)
  - C: Brand colors (8 hex values: bg, bg-deep, ink, ink-soft, rule, accent, red, green). If agent gives <8, suggest tasteful defaults for the rest based on what they provided.
  - D: Typography (display + mono, optional body). Validate that font is on Google Fonts before saving.
  - E: Optional asset files (logo, wordmark mark, headshot). Copy to ~/.config/realty-stack/brand-assets/. Save path in brand-kit.md.
  - F: Voice / positioning notes (optional freeform)
  - G: Confirmation — plain-English summary + small inline preview (HTML rendered as text colored block samples + wordmark mock)
  - H: Refinement loop — freeform feedback, iterate until approved. Accept "ship it", "approved", "done", "save it", "looks good", "OK as-is" as save signals.
  - I: Write brand kit file (only after approval). Use Bash to mkdir -p ~/.config/realty-stack/ and ~/.config/realty-stack/brand-assets/. Use Write to save brand-kit.md.
- **"Brand kit file format"** — full Markdown structure per spec with example
- **"Default suggestions when agent provides incomplete data"** — if agent gives 2-3 colors, suggest defaults: derive bg-deep from bg (5-10% darker), derive ink-soft from ink (lighter shade), default rule to bg-deep equivalent
- **"Edge cases"** — table covering: partial colors, non-Google-Fonts choice, missing asset path, oversized asset (>500KB warning), interrupted onboarding, corrupted file, rebrand request
- **"What this skill never does"** — auto-save before approval, fabricate brand assets, skip the Google Fonts check, overwrite an existing brand kit without explicit user re-onboarding
- **Funnel hook footer** (literal text): `✨ Realty Stack v0.0.3 — Realty Brain (FUB-powered always-on AI) coming soon`

3. **Writing style:** imperative/infinitive form throughout body. Third-person in frontmatter description. Lean (~300-400 lines target).

- [ ] **Step 1: Read the spec for full context**

Read `~/Claude/holden-alt/realty-stack/docs/specs/2026-05-17-brand-kit-capture-design.md` sections "Design" through "Edge cases" before writing.

- [ ] **Step 2: Read the voice-draft SKILL.md as pattern reference**

Read `~/Claude/holden-alt/realty-stack/skills/voice-draft/SKILL.md` — this skill follows the same architectural pattern. Match its structure where possible.

- [ ] **Step 3: Write the SKILL.md**

Create `~/Claude/holden-alt/realty-stack/skills/brand-kit-capture/SKILL.md` with all requirements above.

- [ ] **Step 4: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 5: Re-install + inspect**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
claude plugin details realty-stack
```
Expected: "Skills (3)" appears in component inventory (voice-draft, using-realty-stack, brand-kit-capture); brand-kit-capture on-invoke token count is roughly 3-5k.

- [ ] **Step 6: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/brand-kit-capture/SKILL.md
git commit -m "$(cat <<'EOF'
feat: brand-kit-capture skill — one-time visual brand onboarding

Mirrors voice-draft's pattern. Captures colors (8 hex), typography
(display + mono + optional body), wordmark structure, tagline, and
optional logo/wordmark/headshot asset files. Persists to
~/.config/realty-stack/brand-kit.md and ~/.config/realty-stack/brand-assets/.
Required by /cma and every future visual-output skill in the bundle.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Update using-realty-stack overlay to load brand kit

**Files:**
- Modify: `skills/using-realty-stack/SKILL.md`

- [ ] **Step 1: Read current overlay**

Read `~/Claude/holden-alt/realty-stack/skills/using-realty-stack/SKILL.md` to find the "What this skill does" section (currently has voice profile load as step 4).

- [ ] **Step 2: Add brand-kit load step after voice profile load**

In the "What this skill does" section, insert a new step AFTER the existing step 4 (voice profile load) and renumber subsequent steps:

```markdown
5. **Load the realtor's brand kit** from `~/.config/realty-stack/brand-kit.md` if it exists. Inject the contents into context so every Realty Stack visual-output skill (like /cma) can produce branded output without re-asking for colors/fonts/wordmark.
   - **If the file is missing:** Print a one-line acknowledgment: "(No brand kit loaded — visual-output skills will trigger brand-kit-capture inline.)" Then proceed without blocking. Any visual-output skill invoked later will run brand-kit-capture onboarding inline before completing the original request.
   - **If the file is corrupted** (not parseable as Markdown with expected sections — Wordmark, Colors, Typography): print a friendly note ("Your brand kit looks corrupted — re-running onboarding") and invoke brand-kit-capture.
```

Renumber the subsequent steps (the "Announces..." and "Confirms loaded..." steps) to be steps 6 and 7.

- [ ] **Step 3: Update the compliance baseline section**

Find the section listing what the overlay loads (currently has voice-guide, constitution, fair-housing, voice-profile). Add brand-kit alongside:

```markdown
Every contact-facing output checked against:
- Brand voice tenets (`knowledge/voice-guide.md`)
- Realty Stack constitution (`knowledge/constitution.md`)
- Fair Housing Act + state extensions (`knowledge/fair-housing.md`)
- The realtor's captured voice profile (`~/.config/realty-stack/voice-profile.md` — loaded if present; if absent, onboarding triggers)
- The realtor's captured brand kit (`~/.config/realty-stack/brand-kit.md` — loaded if present; if absent, visual-output skills trigger onboarding)
- NAR Code of Ethics (future: `knowledge/nar-code-of-ethics.md`)
- RESPA basics (future: `knowledge/respa-basics.md`)
- TCPA windows (future: `knowledge/tcpa-windows.md`)
- State disclosures (launch state Michigan; future: `knowledge/disclosure-michigan.md`)
```

- [ ] **Step 4: Validate**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```

- [ ] **Step 5: Re-install + inspect**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
claude plugin details realty-stack
```
Expected: using-realty-stack on-invoke token count increased slightly (~+200 tokens from the new step).

- [ ] **Step 6: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/using-realty-stack/SKILL.md
git commit -m "$(cat <<'EOF'
feat: overlay loads brand kit at session start

Adds brand-kit.md loading to using-realty-stack overlay so every Realty
Stack visual-output skill inherits the agent's brand without per-skill
loading code. Graceful fallback when file missing (visual-output skills
trigger brand-kit-capture inline) or corrupted.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Document brand kit contract in CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read current CLAUDE.md**

Read `~/Claude/holden-alt/realty-stack/CLAUDE.md` to find the "Voice profile contract" section.

- [ ] **Step 2: Add "Brand kit contract" section after Voice profile contract**

Insert a new section after the "Voice profile contract" section's "What every Realty Stack drafting skill MUST NOT do" subsection, before whatever section follows (likely "Testing rules"):

```markdown
## Brand kit contract

Every Realty Stack session loads the realtor's brand kit from `~/.config/realty-stack/brand-kit.md` via the `using-realty-stack` overlay. The file format and full spec live in `docs/specs/2026-05-17-brand-kit-capture-design.md`. Summary of what each brand kit contains:

- **Wordmark** — left segment, separator, right segment (for CSS-rendered HTML text wordmark)
- **Tagline** — agent's positioning line (optional)
- **Colors** — 8 hex values: bg, bg-deep, ink, ink-soft, rule, accent, red, green
- **Typography** — display font (Google Fonts), mono font, optional body font
- **Asset files** — optional paths to logo, wordmark mark, headshot (stored in `~/.config/realty-stack/brand-assets/`)
- **Voice / positioning notes** — freeform brand discipline notes

### What every Realty Stack visual-output skill MUST do

1. **Assume the brand kit is in context.** Don't ask the agent for colors/fonts/wordmark. They onboarded once via brand-kit-capture.
2. **Use the captured colors** for every background / text / border / accent decision in generated HTML.
3. **Use the captured typography** for all text rendering.
4. **Render the wordmark as CSS-styled HTML text** (sharp at any resolution, no image dependency).
5. **Base64-embed asset files** (logo, headshot) in generated HTML for true self-containment (works when emailed, hosted, printed).
6. **Fail gracefully if the brand kit is missing.** Detect the absence, run brand-kit-capture inline to onboard, then complete the agent's original request. Never produce un-branded output silently.

### What every Realty Stack visual-output skill MUST NOT do

- Ask the agent to provide colors, fonts, wordmark, or assets every invocation
- Use a default brand or another agent's brand
- Reference asset files by path in HTML output (breaks self-containment) — always base64-embed
- Persist anything to `~/.config/realty-stack/brand-kit.md` or `~/.config/realty-stack/brand-assets/` — that's brand-kit-capture's exclusive responsibility
- Use brass / accent as a background fill (it's a pigment, not a fill — single-character / thin-bar / single-decorative-element only per the design discipline)
```

- [ ] **Step 3: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: add brand kit contract for visual-output skills

Documents the interface every Realty Stack visual-output skill must follow
when consuming the captured brand kit. Pointer to the full spec in
docs/specs/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: End-to-end test brand-kit-capture with Holden's real brand

**Files:** None modified; verification only.

This is the human-in-loop validation step. Holden runs the full flow to confirm the skill works end-to-end and produces a valid brand-kit.md file that matches his real brand.

- [ ] **Step 1: Clean state**

```bash
rm -f ~/.config/realty-stack/brand-kit.md
rm -rf ~/.config/realty-stack/brand-assets/
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
```

(Do NOT delete `~/.config/realty-stack/voice-profile.md` — Holden's voice profile from v0.0.2 should stay.)

- [ ] **Step 2: Holden opens a fresh Claude Code session**

Open a new terminal, run `claude`. SessionStart hook should fire with the brand-kit-only prompt (voice profile exists, brand kit doesn't).

- [ ] **Step 3: Holden runs onboarding with his real brand**

Walk through:
- Tagline: "Holden/GR — Ambassador To RealSavvy"
- Wordmark: Holden / GR (with brass slash per the 6333 Blackmar design system)
- Colors (the 8 from his existing 6333 Blackmar CSS variables):
  - bg: #F4F3EF
  - bg-deep: #E8E6DF
  - ink: #111418
  - ink-soft: #3A3F46
  - rule: #C7C4BC
  - accent: #B08A44 (brass)
  - red: #963c2a
  - green: #3d6b3d
- Typography: Inter (display, weights 400/500/600/700) + JetBrains Mono (mono, weights 400/500)
- Assets: any logo SVG / headshot Holden has on hand (or skip if none ready)
- Voice/positioning notes: copy the brand discipline from his spec ("Brass is a pigment not a fill...")

- [ ] **Step 4: Verify brand kit file written correctly**

```bash
ls -la ~/.config/realty-stack/brand-kit.md
cat ~/.config/realty-stack/brand-kit.md
```
Expected: file exists; all 8 colors present with correct hex values; typography section has Inter + JetBrains Mono; wordmark section has Holden / GR with brass separator; asset paths (if any provided) are valid.

- [ ] **Step 5: Verify overlay loads brand kit on next session**

Open another fresh Claude Code session. Ask: *"What are my brand colors per the brand kit?"*
Expected: Claude responds with the 8 hex values, proving the overlay loaded the brand kit into context.

- [ ] **Step 6: Final plugin validation**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
claude plugin details realty-stack
```
Expected: validation passes; Skills (3), Hooks (1).

- [ ] **Step 7: Commit any minor fixes (only if needed)**

If onboarding surfaced any typos, missing trigger phrases, or workflow rough edges, commit fixes. Otherwise skip.

---

## Self-review

Plan written and self-checked:

1. **Spec coverage:**
   - UX flow (spec §Design Steps A-I) → Task 1
   - Brand kit file format (spec §"Brand kit file format") → Task 1
   - Consumption by other skills (spec §"Consumption by other skills") → Tasks 2, 3
   - Edge cases (spec §"Edge cases") → Task 1
   - Trigger mechanism (spec §"Triggers") → Task 0 (hook expansion) + Task 1 (skill body)
   - Asset handling (spec §Step E) → Task 1

2. **Placeholder scan:** No "TBD", "TODO", "implement later", or vague "handle appropriately" patterns. All steps contain concrete content (file paths, exact code, exact commands).

3. **Type / path consistency:**
   - `~/.config/realty-stack/brand-kit.md` used consistently throughout (8+ references, all identical)
   - `~/.config/realty-stack/brand-assets/` used consistently for asset storage
   - `skills/brand-kit-capture/SKILL.md` path consistent
   - `check-realty-stack-setup.sh` (renamed from check-voice-profile.sh) — renamed in Task 0, referenced consistently in subsequent tasks
   - Skill name `brand-kit-capture` consistent (no drift to `brand-capture` or `kit-capture`)

4. **Task ordering:** Logical — Task 0 expands hook infrastructure (renamed script + hooks.json update), Task 1 writes the skill itself, Tasks 2-3 wire it into the overlay + document the contract, Task 4 validates end-to-end with Holden's real brand.

5. **Commit hygiene:** Each task ends in one commit. Co-Authored-By footer on each.

6. **Realty Brain tagline:** Uses the corrected v0.0.3 wording ("Realty Brain (FUB-powered always-on AI) coming soon") — no realtybrain.com URL.

No issues found. Ready for execution.
