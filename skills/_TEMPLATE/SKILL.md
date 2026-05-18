---
name: your-skill-name-here
description: This skill should be used when a real estate agent asks to "<trigger phrase 1>", "<trigger phrase 2>", or "<trigger phrase 3>". One-sentence description of what it does and where it persists output (if anywhere). Under ~200 chars for clean Claude routing.
version: 0.0.1
---

# Your Skill — One-Line Tagline

<!-- TODO: Replace this with 2-3 sentences:
     - what this skill does
     - who it's for (most likely: residential real estate agents)
     - where it fits in the bundle (intake / drafting / visual-output / etc.) -->

---

## When this skill runs

<!-- TODO: List the trigger phrases verbatim from your frontmatter description. -->

- "<trigger phrase 1>"
- "<trigger phrase 2>"
- "<trigger phrase 3>"

<!-- TODO: If your skill is invoked inline by other skills as a fallback, 
     document that here. 
     
     Example: "If /xyz is invoked and the X state file is missing, /xyz 
     runs this skill inline before continuing." -->

---

## Pre-checks

<!-- TODO: If your skill consumes state files (voice profile, brand kit, 
     other skill templates), verify they exist. Run the relevant pre-req 
     skill inline if missing.
     
     Pattern reference: skills/cma/SKILL.md "Profile + brand kit pre-checks"
     
     DELETE THIS SECTION if your skill doesn't consume any state files. -->

Before doing any work, verify pre-requisites loaded by the overlay:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion, then return.
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion, then return.

---

## Step 0 — State scan

<!-- TODO: If your skill is an INTAKE skill (asks the realtor for material — 
     content, settings, preferences), you MUST scan canonical realty-stack 
     state locations BEFORE asking. Per CLAUDE.md State scan contract.
     
     Pattern reference: skills/listing-presentation-template/SKILL.md Step 0
     
     DELETE THIS SECTION if your skill doesn't ask for new material 
     (i.e., it's a per-invocation drafting/output skill that only uses 
     existing state). -->

Before asking the realtor for material, scan canonical realty-stack state locations per CLAUDE.md State scan contract:

```bash
ls ~/.config/realty-stack/voice-profile.md ~/.config/realty-stack/brand-kit.md ~/.config/realty-stack/listing-presentation-template.md ~/.config/realty-stack/buyer-presentation-template.md 2>/dev/null
ls ~/Downloads/*-listing-presentation.{html,pdf} ~/Downloads/*-cma.{html,pdf} 2>/dev/null
```

For each found artifact, identify what's relevant to THIS skill's intake. Build an inventory.

**If nothing inheritable found:** fall through silently to Step A.

**If inheritable artifacts found:** report in plain English. Example:

> *"Found your [artifact]. I can pre-populate [X of N fields] from there. Want me to do that, then ask about the remaining [N-X]?"*

If yes → pre-populate, skip to Step D (gap-fill).
If no → fall through to Step A.

---

## Onboarding workflow (or per-invocation workflow)

<!-- TODO: Replace with your skill's actual workflow. Use lettered steps 
     (A, B, C...) for intake skills, numbered steps (1, 2, 3...) for 
     per-invocation skills. Each step should have:
     - A clear action
     - The realtor-facing copy verbatim (if asking a question)
     - Edge case handling inline where relevant
     
     Pattern references:
     - Consultative builder (lettered): skills/listing-presentation-template/SKILL.md (Steps A-H)
     - Per-invocation (numbered): skills/cma/SKILL.md (Steps 1-8)
     - Lighter per-invocation: skills/listing-presentation/SKILL.md (Steps 1-5) -->

### Step A — <step name>

<!-- describe what this step does + the realtor-facing copy if any -->

### Step B — <step name>

<!-- ... -->

---

## Artifact output (visual-output skills only)

<!-- TODO: If your skill produces an HTML artifact, you MUST also produce a 
     PDF via the shared script. Per CLAUDE.md Artifact output contract.
     
     Pattern reference: skills/listing-presentation/SKILL.md Step 5
     
     DELETE THIS SECTION if your skill doesn't produce visual artifacts. -->

After the HTML is written, render the PDF:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render-pdf.sh <html-path> <pdf-path>
```

Confirm BOTH paths back to the realtor in a single message:

> *"Saved to ~/Downloads/{slug}.html (browser preview) and ~/Downloads/{slug}.pdf (print/email-ready)."*

Chrome-missing fallback per the canonical contract: write HTML anyway, tell the realtor to install Chrome or use Cmd+P.

---

## Edge cases

<!-- TODO: Table of edge cases + how this skill handles each. 
     
     Pattern reference: every existing SKILL.md has an "Edge cases" table — 
     copy the format. -->

| Situation | Behavior |
|---|---|
| <edge case 1> | <how the skill handles it> |
| <edge case 2> | <how the skill handles it> |

---

## What this skill never does

<!-- TODO: Bulleted list of explicit prohibitions. Common ones to consider 
     (delete any that don't apply, add skill-specific ones):
     
     - Auto-send anything to clients (T18: show before do)
     - Fabricate market data, stats, or testimonials
     - Generate "exclusive listing" / "off-market" / "private listing" 
       language unless the realtor explicitly confirms the listing has 
       that status (per CLAUDE.md Do-Not list)
     - Persist anything to state files owned by other skills
     - Use a default brand or another agent's brand (always the active brand kit)
     - Mix Text Voice with Email Voice
     - Make pricing/DOM/savings guarantees -->

- ...
- ...

---

## Funnel hook

<!-- IMPORTANT: This footer line MUST appear as the final line of every 
     skill output. The version number gets bumped during release cycles — 
     check the current VERSION file. -->

At end of every output this skill produces, append:

`✨ Realty Stack v0.0.5 — Realty Brain (FUB-powered always-on AI) coming soon`
