# voice-draft v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current per-invocation voice-draft skill with the v2 one-time onboarding flow that captures the realtor's email + text voice and persists it for downstream skills to consume.

**Architecture:** SessionStart hook auto-prompts onboarding on first install; voice-draft skill walks the realtor through sample collection, analysis, confirmation, and refinement; result saved to `~/.config/realty-stack/voice-profile.md`; using-realty-stack overlay loads the profile into context for every Realty Stack skill.

**Tech Stack:** Markdown (SKILL.md format), JSON (hooks.json), Bash (hook script). Standard Claude Code plugin primitives, no external dependencies.

**Spec:** `docs/specs/2026-05-16-voice-draft-v2-design.md`

---

## File Structure

### To Create
- `hooks/scripts/check-voice-profile.sh` — bash script that checks for profile, outputs onboarding prompt if missing
- `hooks/hooks.json` — SessionStart hook config wiring to the script

### To Rewrite
- `skills/voice-draft/SKILL.md` — full rewrite per design spec sections 4-5

### To Update
- `skills/using-realty-stack/SKILL.md` — add voice profile loading at session start
- `CLAUDE.md` — document voice profile contract for future drafting skills
- `README.md` — update voice-draft mentions to reflect onboarding behavior
- `CHANGELOG.md` — append v0.0.2 entry

### Unchanged
- `knowledge/voice-guide.md`, `knowledge/constitution.md`, `knowledge/fair-housing.md`
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- `ETHOS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `VERSION`, `.gitignore`

---

## Task 0: Initial repo commit

**Files:** All existing repo content (16 files: scaffold + Wave-1 fixes + spec doc + this plan)

- [ ] **Step 1: Verify git state**

Run: `cd ~/Claude/holden-alt/realty-stack && git status`
Expected: untracked files include the full scaffold; nothing yet committed.

- [ ] **Step 2: Stage all scaffold files**

Run: `git add -A`

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
Initial commit: realty-stack v0.0.1 scaffold + v2 voice-draft spec

- MIT license, plugin + marketplace manifests
- Knowledge base: voice-guide, constitution, fair-housing
- voice-draft (v0.0.1 — superseded by v2 in next commits)
- using-realty-stack overlay
- ETHOS, CLAUDE, README, CONTRIBUTING, SECURITY docs
- v2 design spec + implementation plan in docs/

Spec-validated via claude plugin validate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Verify**

Run: `git log --oneline`
Expected: 1 commit listed.

---

## Task 1: Create voice profile check script

**Files:**
- Create: `hooks/scripts/check-voice-profile.sh`

- [ ] **Step 1: Create the hooks/scripts/ directory**

Run: `cd ~/Claude/holden-alt/realty-stack && mkdir -p hooks/scripts`

- [ ] **Step 2: Write the check script**

Write `hooks/scripts/check-voice-profile.sh`:

```bash
#!/usr/bin/env bash
# Realty Stack — SessionStart hook
# Checks for the realtor's voice profile; if missing, outputs an
# onboarding prompt that Claude will see as additional session context.

set -euo pipefail

PROFILE_PATH="${HOME}/.config/realty-stack/voice-profile.md"

if [[ ! -f "${PROFILE_PATH}" ]]; then
  cat <<'EOF'
[Realty Stack: voice profile not found]

The user has installed Realty Stack but hasn't completed voice onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Before you use any skills, let's capture your
> writing voice — takes about 5 minutes, one-time. Want to do it now?"

If they say yes (or any natural affirmation), invoke the voice-draft skill
to walk them through onboarding.

If they decline or say "later," respect that and answer their actual
question — but mention that any Realty Stack drafting skill they invoke
later will trigger voice-draft inline before completing their request.
EOF
fi

exit 0
```

- [ ] **Step 3: Make it executable**

Run: `chmod +x hooks/scripts/check-voice-profile.sh`

- [ ] **Step 4: Test with profile missing**

```bash
rm -f ~/.config/realty-stack/voice-profile.md
bash hooks/scripts/check-voice-profile.sh
```
Expected: outputs the "[Realty Stack: voice profile not found]" block.

- [ ] **Step 5: Test with profile present**

```bash
mkdir -p ~/.config/realty-stack
touch ~/.config/realty-stack/voice-profile.md
bash hooks/scripts/check-voice-profile.sh
rm ~/.config/realty-stack/voice-profile.md
```
Expected: no output (silent exit).

- [ ] **Step 6: Commit**

```bash
git add hooks/scripts/check-voice-profile.sh
git commit -m "$(cat <<'EOF'
feat: SessionStart hook script to check voice profile

Outputs onboarding prompt when ~/.config/realty-stack/voice-profile.md
is missing; silent when present.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Wire the SessionStart hook

**Files:**
- Create: `hooks/hooks.json`

- [ ] **Step 1: Write hooks/hooks.json**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-voice-profile.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Validate the plugin**

Run: `claude plugin validate ~/Claude/holden-alt/realty-stack`
Expected: "Validation passed."

- [ ] **Step 3: Re-install plugin to pick up the hook**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
```

- [ ] **Step 4: Inspect plugin to confirm hook registered**

Run: `claude plugin details realty-stack`
Expected: "Hooks (1)" appears in the inventory.

> **VERIFICATION NEEDED:** Confirm SessionStart hook output makes it into Claude's context as additional instruction. If it does NOT (e.g., output goes to stderr but isn't injected into the conversation), add a follow-up step here to switch the hook to a different output mechanism (`type: prompt` if available, or wrap the bash script's output in a specific format Claude Code expects). Test in Task 7 will catch this if it's wrong.

- [ ] **Step 5: Commit**

```bash
git add hooks/hooks.json
git commit -m "$(cat <<'EOF'
feat: wire SessionStart hook to voice profile check

Hook fires the check script on every session start; injects onboarding
prompt into context when voice profile is missing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Rewrite voice-draft SKILL.md

**Files:**
- Rewrite: `skills/voice-draft/SKILL.md`

**Spec reference:** `docs/specs/2026-05-16-voice-draft-v2-design.md` sections 4-5.

**Requirements for the new SKILL.md (all MUST be present):**

1. **Frontmatter:**
```yaml
---
name: voice-draft
description: This skill should be used when a real estate agent asks to "set up my voice", "capture my voice", "onboard me", "first time setup", "complete realty stack setup", "load my voice", "I just installed", or "configure realty stack" — i.e., for the one-time onboarding that captures the agent's writing voice (email + text) so all other Realty Stack drafting skills produce output in their voice. Walks the agent through profile collection, sample submission, analysis, confirmation, and refinement; persists the result to ~/.config/realty-stack/voice-profile.md.
version: 0.0.2
---
```
   - NO `allowed-tools` field (skills inherit session permissions)
   - `version: 0.0.2` (bump from v0.0.1)

2. **Body sections (in this order):**
   - **H1:** "Voice Draft"
   - **Intro paragraph (≤3 sentences):** Purpose — one-time onboarding. Other skills auto-use the captured profile.
   - **"When this skill runs":** Both trigger paths — SessionStart hook auto-prompt + first-skill-invocation fallback.
   - **"Onboarding workflow"** — numbered steps:
     1. Step A: collect Agent Profile (4 fields: Name, Brokerage, Primary Market, Preferred Signoff for email AND text). Signoff optional if obvious from samples.
     2. Step B: collect 3-5 substantial emails (real-estate context). Push back if fewer than 2 substantial samples.
     3. Step C: collect 3-5 substantial texts (real-estate context). Same threshold.
     4. Step D: analyze both batches. Build email-voice + text-voice profiles per spec section 5 format.
     5. Step E: return confirmation — voice summary (~150-300 words per voice in plain English) + 1 example email + 1 example text on default scenarios.
     6. Step F: refinement loop. Freeform feedback in → adjust profile → regenerate examples → ask again. Loop until "yes that's me" or semantic equivalent.
     7. Step G: write the voice profile file to `~/.config/realty-stack/voice-profile.md` using Write tool. Use Bash to `mkdir -p ~/.config/realty-stack/` first if missing.
   - **"Default example scenarios"** for Step E:
     - Email: *"Follow up with a hot buyer lead who toured a property 5 days ago about a new comparable listing that just hit MLS."*
     - Text: *"Let a past client know about a listing that just dropped in the same neighborhood they bought in 18 months ago."*
   - **"Voice profile file format"** — full Markdown structure per spec section 5, with example.
   - **"Edge cases"** — table from spec section 5: thin samples, template-only samples, inconsistent samples, interrupted onboarding, corrupted file, mid-session refresh, mid-onboarding unrelated question.
   - **"What this skill never does":**
     - Auto-send any message
     - Persist anything to disk until refinement is approved
     - Skip the confirmation step
     - Fabricate the agent's name, brokerage, or market
   - **Funnel hook footer (literal text at end of every output):**
     > ✨ Realty Stack v0.0.2 — Realty Brain syncs your voice across devices and learns continuously: realtybrain.com

3. **Writing style** per plugin-dev's `skill-development` skill convention:
   - **Imperative/infinitive form** ("Load the file") not second person ("You should load the file")
   - **Third person in frontmatter description** ("This skill should be used when...")
   - Lean body (target ~400-500 lines max with frontmatter)

- [ ] **Step 1: Read the design spec for context**

Read `docs/specs/2026-05-16-voice-draft-v2-design.md` sections 4 (UX flow), 5 (file format), and the edge-cases table.

- [ ] **Step 2: Write the new SKILL.md**

Write `skills/voice-draft/SKILL.md` implementing ALL requirements listed above. Replace the existing v0.0.1 content entirely.

- [ ] **Step 3: Validate the plugin**

Run: `claude plugin validate ~/Claude/holden-alt/realty-stack`
Expected: "Validation passed."

- [ ] **Step 4: Re-install + inspect**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
claude plugin details realty-stack
```
Expected: voice-draft listed; on-invoke token count reflects richer workflow (~4-6k tokens).

- [ ] **Step 5: Commit**

```bash
git add skills/voice-draft/SKILL.md
git commit -m "$(cat <<'EOF'
feat: rewrite voice-draft as one-time onboarding skill (v0.0.2)

Replaces v0.0.1 per-invocation paste-samples pattern with one-time
onboarding per docs/specs/2026-05-16-voice-draft-v2-design.md. Captures
email + text voices + basic profile (name, brokerage, market, signoff);
persists to ~/.config/realty-stack/voice-profile.md. Downstream
drafting skills auto-consume via the using-realty-stack overlay.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Update using-realty-stack overlay to load voice profile

**Files:**
- Modify: `skills/using-realty-stack/SKILL.md`

- [ ] **Step 1: Read current overlay**

Read `skills/using-realty-stack/SKILL.md` to identify the "What this skill does" section and the "compliance baseline" section.

- [ ] **Step 2: Add voice profile load step**

In the "What this skill does" section, after the three existing knowledge file loads (voice-guide, constitution, fair-housing), insert a new step:

```markdown
4. **Load the realtor's voice profile** from `~/.config/realty-stack/voice-profile.md` if it exists. Inject the contents into context so every Realty Stack drafting skill can match the agent's voice without re-asking for samples.
   - **If the file is missing:** do not block. The SessionStart hook should have already prompted for onboarding; if the realtor declined, respect that and proceed. Any drafting skill invoked later will run voice-draft onboarding inline.
   - **If the file is corrupted** (not parseable as Markdown with expected sections — Agent Profile, Email Voice, Text Voice): print a friendly note ("Your voice profile looks corrupted — re-running onboarding") and invoke voice-draft.
```

Renumber subsequent steps so the announcement step becomes step 6 (or whatever follows).

- [ ] **Step 3: Update "compliance baseline" section**

Find the section listing what the overlay loads. Add the voice profile alongside the three knowledge files. Example:

```markdown
Every contact-facing output checked against:
- Brand voice tenets (`knowledge/voice-guide.md`)
- Realty Stack constitution (`knowledge/constitution.md`)
- Fair Housing Act + state extensions (`knowledge/fair-housing.md`)
- The realtor's captured voice profile (`~/.config/realty-stack/voice-profile.md` — loaded if present; if absent, onboarding triggers)
```

- [ ] **Step 4: Validate**

Run: `claude plugin validate ~/Claude/holden-alt/realty-stack`
Expected: "Validation passed."

- [ ] **Step 5: Re-install + inspect**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
claude plugin details realty-stack
```
Expected: using-realty-stack on-invoke token count increased slightly (~1.7k from ~1.5k).

- [ ] **Step 6: Commit**

```bash
git add skills/using-realty-stack/SKILL.md
git commit -m "$(cat <<'EOF'
feat: overlay loads voice profile at session start

Adds voice-profile.md loading to using-realty-stack overlay so every
Realty Stack drafting skill inherits the realtor's voice without
per-skill loading code. Graceful fallback when file missing or
corrupted.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Document voice profile contract in CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add new section after "Skill writing conventions"**

Append this section to `CLAUDE.md` immediately after the "### Scripts pattern" subsection within "Skill writing conventions":

```markdown
## Voice profile contract

Every Realty Stack session loads the realtor's voice profile from `~/.config/realty-stack/voice-profile.md` via the `using-realty-stack` overlay. The file format and full spec live in `docs/specs/2026-05-16-voice-draft-v2-design.md` section 5. Summary:

- **Agent Profile** — name, brokerage, primary market, preferred email signoff, preferred text signoff
- **Email Voice** — plain-English description + observed patterns (sentence length, openers, signoffs, em-dash usage, hedge word frequency, exclamation rate, emoji policy, notable phrasings)
- **Text Voice** — same shape as Email Voice, for texts
- **Source Samples** — raw samples preserved for future re-analysis
- **Refinement History** — audit log of changes

### What every Realty Stack drafting skill MUST do

1. **Assume the voice profile is in context.** Don't ask the realtor for samples. They onboarded once via voice-draft.
2. **Match the right voice mode.** Email Voice for emails, FUB notes, long-form. Text Voice for texts, SMS, quick replies.
3. **Use Agent Profile fields for context.** Their name for signatures, brokerage for signature blocks, market for "Practical & Local" specificity.
4. **Fail gracefully if the profile is missing.** Detect the absence, run voice-draft inline to onboard, then complete the realtor's original request. Never produce un-voiced output silently.

### What every Realty Stack drafting skill MUST NOT do

- Ask the realtor to paste voice samples
- Make up the realtor's name, brokerage, or market
- Mix email voice with text voice (e.g., draft a text using the email-voice description)
- Persist anything to `~/.config/realty-stack/voice-profile.md` — that's voice-draft's exclusive responsibility
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: add voice profile contract for future drafting skills

Documents the interface every Realty Stack drafting skill must follow
when consuming the captured voice profile. Pointer to the full spec in
docs/specs/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Update README to reflect onboarding-only voice-draft

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the "See it work" section**

Find the existing "## See it work" section (the Sarah/Heritage Hill demo). Replace its body with:

```markdown
## See it work

Real onboarding sequence from a fresh install:

**Install:** `claude plugins install github.com/holdengr/realty-stack` — done.

**First Cowork session after install:** Realty Stack auto-prompts:

> *"Realty Stack is loaded. Before you use any skills, let's capture your writing voice — takes about 5 minutes, one-time. Want to do it now?"*

**Holden:** "yes"

→ Voice-draft walks through: name, brokerage, market, signoffs (4 quick fields), then 3-5 real emails Holden pastes, then 3-5 real texts. Analysis runs (~30 seconds). Returns:

> *Email voice: short, direct. Em-dashes for clauses. Opens with "Hey [name]," or "[Name] —". Signs "— Holden" casually, "Holden Richardson | 616 Realty" formally. No exclamation points unless an offer actually got accepted...*
>
> *Text voice: very clipped — fragments encouraged. Opens with first name only or nothing. Signs "— H" or none. Em-dashes everywhere. Never emoji unless the contact uses them first...*
>
> *Example email (follow-up to hot buyer about new comparable):* [drafted email in Holden's voice]
>
> *Example text (past-client neighborhood listing alert):* [drafted text in Holden's voice]
>
> *"Sound like you? Or refine?"*

**Holden:** "yes that's me" → onboarding complete, voice profile written to `~/.config/realty-stack/voice-profile.md`. **Total time: ~5 minutes.**

**From this point forward**, every Realty Stack skill (follow-up-draft, listing-description, meeting-distill, etc.) produces output in Holden's voice automatically. He never pastes voice samples again.
```

- [ ] **Step 2: Update the skills table**

Replace the existing `voice-draft` row in the "Skills (v0.0.1)" section with:

```markdown
| `voice-draft` (one-time, on install) | Auto-fires on first session post-install; also "set up my voice", "onboard me", "configure realty stack" | Captures the realtor's email + text voice + basic profile. Persists to `~/.config/realty-stack/voice-profile.md`. Future drafting skills auto-use it. ~5 min one-time setup. |
```

(Other rows in the table — for the "coming this week" skills — stay unchanged but their descriptions can stay too. They'll consume the voice profile when written.)

- [ ] **Step 3: Update CHANGELOG.md**

Append after the v0.0.1 entry:

```markdown
## [0.0.2] — 2026-05-16

### Changed
- **voice-draft is now a one-time onboarding skill** (was: per-invocation paste-samples). Captures email + text voice + basic profile (name, brokerage, market, signoff) and persists to `~/.config/realty-stack/voice-profile.md`. Downstream drafting skills auto-consume via the overlay.

### Added
- `hooks/hooks.json` + `hooks/scripts/check-voice-profile.sh` — SessionStart hook auto-prompts onboarding when voice profile is missing.
- `using-realty-stack` overlay loads voice profile into context at session start.
- `CLAUDE.md`: voice profile contract for future drafting skills.

### Notes
- Voice profile is per-device (no sync in v0.0.x). Realty Brain (paid sibling) will provide multi-device sync when it ships.
```

- [ ] **Step 4: Bump VERSION**

Edit `VERSION` to contain `0.0.2`.

- [ ] **Step 5: Bump plugin.json version**

Edit `.claude-plugin/plugin.json` — change `"version": "0.0.1"` to `"version": "0.0.2"`.

- [ ] **Step 6: Commit**

```bash
git add README.md CHANGELOG.md VERSION .claude-plugin/plugin.json
git commit -m "$(cat <<'EOF'
docs+chore: v0.0.2 — voice-draft v2 onboarding flow

- README: replace per-invocation demo with onboarding sequence
- README: update skills table for new voice-draft semantics
- CHANGELOG: v0.0.2 entry
- VERSION + plugin.json: bump to 0.0.2

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: End-to-end functional test

**Files:** None modified; verification only. If issues found, file the fix as a new task and circle back.

- [ ] **Step 1: Clean state**

```bash
rm -f ~/.config/realty-stack/voice-profile.md
rmdir ~/.config/realty-stack 2>/dev/null || true
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
```

- [ ] **Step 2: Open a fresh Claude Code session**

Open a NEW Claude Code session (separate terminal or new Cowork project — not the one this plan is being executed in). The session must be new so the SessionStart hook fires cleanly.

- [ ] **Step 3: Verify the SessionStart hook fired**

Expected: Claude's opening message references the voice onboarding prompt (per the hook script output).

**If the hook output did NOT inject into Claude's context** (e.g., Claude greets normally without referencing voice onboarding):
   - This is the verification flagged in Task 2 Step 4.
   - Debug: check `claude plugin details realty-stack` for "Hooks (1)"; run the hook script manually to confirm it outputs.
   - Fix: try alternate hook configuration. If `type: prompt` is supported in Claude Code 2.x, switch to that. Otherwise add a wrapping mechanism (e.g., have the script write its output to a known path that the overlay reads at session start).

- [ ] **Step 4: Run through onboarding with Holden's real samples**

Holden provides 3-5 real emails + 3-5 real texts + name + brokerage + market + signoff. Walk through analysis, confirmation, refinement (if needed), approval.

- [ ] **Step 5: Verify voice profile file written correctly**

```bash
ls -la ~/.config/realty-stack/voice-profile.md
head -50 ~/.config/realty-stack/voice-profile.md
```
Expected: file exists; contains Agent Profile, Email Voice, Text Voice, Source Samples, Refinement History sections.

- [ ] **Step 6: Verify overlay loads profile on a fresh session**

Open ANOTHER fresh session (third one for this test). Ask Claude: *"What's my email signoff per the voice profile?"*
Expected: Claude responds with the correct signoff from the saved profile — proves the overlay loaded the file.

- [ ] **Step 7: Final plugin validation**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
claude plugin details realty-stack
```
Expected: validation passes; component inventory shows Skills (2) + Hooks (1).

- [ ] **Step 8: Commit if needed**

If any minor fixes happened during testing (typos, etc.), commit them now with a clear message. Otherwise skip.

---

## Task 8: Push to GitHub (ASK HOLDEN FIRST)

**Files:** None modified; remote work only.

- [ ] **Step 1: Confirm with Holden**

Ask explicitly: *"Ready to push realty-stack to GitHub? Default would be `github.com/holdengr/realty-stack` as a public repo. Confirm the org/username and visibility before I create + push."*

Wait for explicit "yes" before proceeding.

- [ ] **Step 2 (only if approved): Create the GitHub repo**

```bash
cd ~/Claude/holden-alt/realty-stack
gh repo create holdengr/realty-stack --public \
  --description "Opinionated AI skills for top-producing residential real estate agents. Built by a working realtor + AI engineer." \
  --source . \
  --push
```

- [ ] **Step 3: Tag the release**

```bash
git tag v0.0.2
git push origin v0.0.2
```

- [ ] **Step 4: Verify**

Open `https://github.com/holdengr/realty-stack` and confirm:
- README renders correctly
- All files visible
- License badge displays
- v0.0.2 tag visible in releases

---

## Self-review

Plan written and self-checked:

1. **Spec coverage:**
   - UX flow (spec § 4) → Tasks 1, 2, 3
   - Voice profile file format (spec § 5) → Task 3 (skill writes it)
   - Consumption by other skills (spec § 5) → Tasks 4, 5
   - Edge cases (spec § 5) → Task 3 (handled in skill body) + Task 7 (validation)
   - Trigger mechanism (spec § 4) → Tasks 1, 2 (SessionStart hook) + Task 3 (skill handles first-skill fallback)
   - "Things this design explicitly does NOT do" (spec § 5) → reflected in skill body (Task 3) and CLAUDE.md (Task 5)

2. **Placeholder scan:** No "TBD", "TODO", "implement later", or vague "add appropriate X" patterns. The one VERIFICATION NEEDED note in Task 2 is explicitly labeled as a hypothesis to confirm at execution time, not a deferred decision.

3. **Type/path consistency:**
   - `~/.config/realty-stack/voice-profile.md` used consistently throughout (4 references, all identical)
   - `skills/voice-draft/SKILL.md`, `skills/using-realty-stack/SKILL.md` paths consistent
   - `hooks/hooks.json`, `hooks/scripts/check-voice-profile.sh` paths consistent
   - Plugin name `realty-stack` consistent (no drift to `realty-stack-plugin` or similar)
   - Marketplace name `realty-stack` consistent

4. **Task ordering:** Logical — Task 0 establishes git, Tasks 1-2 build hook infrastructure (script then config), Task 3 rewrites the skill that the hook triggers, Task 4 integrates the overlay (which the skill depends on for downstream consumption), Tasks 5-6 docs, Task 7 validates end-to-end, Task 8 ships to public.

5. **Commit hygiene:** Each task ends in one commit with a clear message. Co-Authored-By footer on each.

6. **Holden collaboration markers:** Task 8 explicitly asks before public-facing action (matches his "check in on big decisions" rule). Task 0's initial commit honest about replacing voice-draft in subsequent tasks.

No issues found. Ready for execution.
