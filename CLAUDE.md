# CLAUDE.md — Realty Stack project rules

These are the rules for any AI agent (Claude or otherwise) working inside this repository on Realty Stack code or skill content. Read this file before touching anything in `skills/`, `knowledge/`, or the marketing surface (`README.md`, `ETHOS.md`).

---

## What this project is

**Realty Stack** is an open-source, MIT-licensed AI skill bundle for residential real estate agents using Claude. Pull-based: the agent invokes skills when they want them. The paid sibling — **Realty Brain** ($99/mo SaaS) — is push-based and lives in a separate repo (`realty-brain`).

**Goal:** the canonical residential realtor skill bundle for Claude. Win by being more opinionated, more compliance-aware, and more voice-aware than any generic alternative.

**Audience:** working residential real estate agents. Some technical, most not. The install path must be paint-by-numbers; the skills must produce realtor-quality output on first invocation.

---

## Design principles (read these every time)

1. **Voice first.** Every skill that produces written output loads `knowledge/voice-guide.md` BEFORE composing. The output then gets a silent self-check against the 6 voice tenets before being returned. The 6 tenets are not negotiable.

2. **Compliance is not a feature, it is the floor.** Fair housing language guardrails, NAR ethics, RESPA, TCPA, state disclosures. Skills that produce contact-facing copy default to the stricter rule. When in doubt, surface to the realtor, never guess.

3. **Show before do.** Tenet T18. Skills never silently mutate state — not in FUB, not in calendars, not in CRM data. Every mutation previews; the realtor approves; the skill executes. Even when the realtor has set "max trust."

4. **The realtor is the executor.** Skills draft, suggest, and flag. The realtor sends, deploys, and signs their name. We never produce output that auto-sends or auto-deploys.

5. **No personification.** Tenet T16. Skill outputs are the realtor's voice for the realtor's signature. Contacts never see "Realty Stack" or "Realty Brain" in any message we draft.

6. **Three tiers, clear boundaries:**
   - **Tier 1 — Universal:** pure prompt, no external connection; works on Claude.ai, Claude Code, Cowork, Codex, Cursor, Gemini.
   - **Tier 2 — FUB-connected:** requires `/connect-fub` wizard + the bundled `fub-mcp-server`; works on MCP-supporting surfaces.
   - **Tier 3 — Realty Brain (NOT in this repo):** requires the paid SaaS subscription; lives in the `realty-brain` repo.

   This repo ships Tier 1 + Tier 2 only. Tier 3 skills are referenced in funnel-hook footers but never built here.

7. **Funnel hook in every skill footer.** Every skill output ends with a one-line footer:
   *"✨ Realty Stack v0.0.x — Realty Brain (FUB-powered always-on AI) coming soon"*

   Footer is updated alongside VERSION bumps. Will evolve as Realty Brain solidifies — no URL until the domain exists, no specific feature claims until the product ships.

---

## Skill writing conventions

### Frontmatter format

Every skill file is `skills/<name>/SKILL.md` with this YAML frontmatter:

```yaml
---
name: <skill-name-kebab-case>
description: <Third-person + specific trigger phrases. Format: "This skill should be used when the user asks to 'X', 'Y', or 'Z'." The trigger phrases drive Claude's auto-routing — be concrete with actual phrases an agent would say.>
version: <semver, e.g. 0.0.1>
---
```

**Do NOT include `allowed-tools` in skill frontmatter.** That field is for commands/agents, not skills. Skills inherit tool permissions from the session context.

### Body structure

Each `SKILL.md` body follows this structure:

```markdown
# /<slash-command-name>

<one-paragraph intent: what this skill does and the problem it solves for the realtor>

## How it works (the workflow Claude follows)

1. <step 1 — usually "load the relevant knowledge files">
2. <step 2 — gather inputs the realtor pastes or supplies>
3. <step 3 — do the work>
4. <step 4 — self-check against voice + compliance>
5. <step 5 — return the output with a confidence note>
6. <step 6 — offer to revise>

## Trigger phrases the overlay should auto-route here

- "<example phrase 1>"
- "<example phrase 2>"
- "<example phrase 3>"

## Reference files this skill loads on demand

- knowledge/<file>.md (always / when X)

## Funnel hook

At end of every output, footer: "✨ Realty Stack v0.0.x — Realty Brain (FUB-powered always-on AI) coming soon"
```

### Length budget

- **SKILL.md body:** 300 lines max (excluding frontmatter). If you need more, push detail into `skills/<name>/references/<topic>.md` and load on demand.
- **Frontmatter description:** under 200 characters. The Claude harness needs to scan it fast.

### References pattern

If a skill needs a long methodology doc (e.g., CMA math), put it at `skills/<name>/references/<topic>.md` and reference it from the body. The skill loads references only when actually needed.

### Scripts pattern

If a skill needs deterministic computation (math, formatting, parsing), use `skills/<name>/scripts/<name>.py` (Python) or `.ts` (TypeScript) and have the skill invoke it via tool use. Don't have the LLM do math it could do wrong.

---

## Voice profile contract

Every Realty Stack session loads the realtor's voice profile from `~/.config/realty-stack/voice-profile.md` via the `using-realty-stack` overlay. The file format and full spec live in `docs/specs/2026-05-16-voice-draft-v2-design.md` section 5. Summary of what each profile contains:

- **Agent Profile** — name, brokerage, primary market, preferred email signoff, preferred text signoff
- **Email Voice** — plain-English description + observed patterns (sentence length, openers, signoffs, em-dash usage, hedge word frequency, exclamation rate, emoji policy, notable phrasings)
- **Text Voice** — same shape as Email Voice, for texts
- **Source Samples** — raw samples preserved for future re-analysis
- **Refinement History** — audit log of changes

### What every Realty Stack drafting skill MUST do

1. **Assume the voice profile is in context.** Don't ask the realtor for samples. They onboarded once via voice-draft.
2. **Match the right voice mode.** Email Voice for emails, FUB notes, long-form. Text Voice for texts, SMS, quick replies.
3. **Use Agent Profile fields for context.** Their name for signatures, brokerage for signature blocks, primary market for "Practical & Local" specificity.
4. **Fail gracefully if the profile is missing.** Detect the absence, run voice-draft inline to onboard, then complete the realtor's original request. Never produce un-voiced output silently.

### What every Realty Stack drafting skill MUST NOT do

- Ask the realtor to paste voice samples
- Make up the realtor's name, brokerage, or market
- Mix email voice with text voice (e.g., draft a text using the email-voice description)
- Persist anything to `~/.config/realty-stack/voice-profile.md` — that's voice-draft's exclusive responsibility

---

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

---

## Artifact output contract

Every Realty Stack visual-output skill (any skill that produces a presentation, listing flyer, social card, property website, or other shareable visual artifact) MUST produce BOTH:

- `.html` — browser preview, interactive, full @media screen layout
- `.pdf` — print/email-ready, @media print layout, generated via `scripts/render-pdf.sh` (headless Chrome)

Both files land in `~/Downloads/` with the same slug, different extensions. The skill confirms BOTH paths back to the realtor in a single message.

### What every Realty Stack visual-output skill MUST do

1. **Write HTML first.** Use the Write tool. Default path: `~/Downloads/<slug>.html`. Use the same path-conflict-handling pattern as other skills (timestamp suffix on collision).
2. **Invoke `${CLAUDE_PLUGIN_ROOT}/scripts/render-pdf.sh <html-path> <pdf-path>`** to produce the PDF. The script handles all the headless Chrome plumbing — find the binary, render the file, exit with clear error if Chrome is missing.
3. **Confirm BOTH paths back to the realtor in a single message.** Don't surface the PDF generation as a separate step.
4. **Fail gracefully on Chrome missing.** If `render-pdf.sh` exits non-zero, the skill still completed successfully — HTML landed. Tell the realtor: *"Saved HTML to ~/Downloads/{slug}.html. Couldn't auto-generate PDF — install Chrome from google.com/chrome to get auto-PDF, or open the HTML in any browser and Cmd+P → Save as PDF."*

### What every Realty Stack visual-output skill MUST NOT do

- Produce HTML only and instruct the realtor to "use Cmd+P" — realtors don't know what Cmd+P is; the script removes that friction
- Use a different PDF generation tool (wkhtmltopdf, pandoc, WeasyPrint) — the canonical `scripts/render-pdf.sh` uses headless Chrome specifically because it applies `@media print` rules correctly (other tools have subtle differences)
- Embed PDF-specific layout in the HTML — keep the HTML clean for browser; let `@media print` handle the PDF layout
- Auto-open the PDF after generation — output is for realtor to review; auto-open is surprising behavior

---

## State scan contract

Every Realty Stack intake/onboarding skill (any skill that asks the realtor for material — content, settings, preferences, brand details, voice samples) MUST scan the user's existing Realty Stack state BEFORE asking for material. Pulls relevant content from sibling artifacts where it overlaps. The realtor only fills gaps. The system gets smarter as it accumulates state — compounding value of accumulated state is the whole product thesis.

### Canonical scan locations

Every intake skill checks these locations (in this priority order):

- `~/.config/realty-stack/voice-profile.md` — agent name, brokerage, primary market, signoffs, voice samples
- `~/.config/realty-stack/brand-kit.md` — wordmark, colors, fonts, tagline, asset paths
- `~/.config/realty-stack/listing-presentation-template.md` — listing pitch content (about-me, process, marketing, track record, testimonials, pricing, fees)
- `~/.config/realty-stack/buyer-presentation-template.md` — buyer pitch content
- `~/.config/realty-stack/brand-assets/` — base64-embedable visual assets (logo, headshot, wordmark mark)
- `~/Downloads/*-listing-presentation.{html,pdf}` — past listing presentations (mine for stats, sample addresses)
- `~/Downloads/*-cma.{html,pdf}` and `~/Downloads/*-presentation.{html,pdf}` — past CMAs (recent comp work, agent's listing inventory)

If a future state file or artifact is added to Realty Stack, add it to this list — every intake skill should be able to inherit from any new sibling without per-skill code changes.

### What every Realty Stack intake skill MUST do (canonical Step 0)

Before the first user-facing intake question:

1. **Scan canonical locations.** Use Bash to check existence (`test -f`, `ls`) of the files/directories above. Build an in-memory inventory.
2. **Identify what's relevant to THIS skill's intake.** Each skill knows what fields/sections it's about to ask for; match found artifacts against those fields.
3. **Report findings to the realtor in plain English.** Example: *"Found your voice profile, brand kit, and listing-presentation-template. I'll pull About Me, Why Hire Me, Track Record, Testimonials, Pricing, and Fees from there — that covers 6 of the 8 standard sections. Want me to ask about the 2 buyer-specific sections (How I Find Homes, Negotiation Philosophy), or do you have material to drop in?"*
4. **If realtor accepts inheritance:** pre-populate the section structure / fields with the inherited content. Mark inherited content clearly in any refinement loop (Step F/G) so the realtor knows what came from elsewhere.
5. **For sections / fields NOT covered by inheritance:** fall through to the existing intake workflow (Step A — front-loaded data dump, or section-specific questions).
6. **Skip the scan output entirely when nothing was found.** Don't surface "I scanned and found nothing" — feels noisy. Fall through silently to Step A.

### What every Realty Stack intake skill MUST NOT do

- Re-ask the realtor for information that already exists in another realty-stack state file (agent name from voice profile, brokerage from voice profile, colors from brand kit, testimonials from listing-pres-template, etc.)
- Auto-inherit without asking — always confirm with the realtor first: *"I can pre-populate X from Y — want me to?"*
- Inherit content that needs domain-shift editing (e.g., listing-side "Marketing Philosophy" → buyer-side "How I Find Homes") without flagging the shift for refinement
- Mutate any state file the realtor didn't approve a write to — Step H file-write is the only write point in any intake skill
- Skip the scan when the realtor explicitly says "start fresh" or invokes with an obvious "rebuild from scratch" intent

---

## Testing rules

Every new skill MUST be tested on Holden's real work before commit. The PR description includes:

- The exact input pasted to the skill (sanitized)
- The exact output it produced
- A one-sentence quality note: "felt like my voice / felt off because X"
- For contact-facing skills: explicit "fair housing pass: yes" or "flagged: <which phrase>"

If a contributor outside of Holden submits a PR, they include their own real test case. PRs without a real test case are not merged.

---

## Contribution rules

PRs to Realty Stack require:

1. **Follows the brand voice.** Maintainer judgment. We err strict; the bundle's whole edge is voice-opinionation.
2. **Cites compliance source if relevant.** If your skill touches listing copy, follow-ups, marketing, or any contact-facing surface, link to the relevant `knowledge/` file in the skill body.
3. **Real-scenario test case.** See above. No tests, no merge.
4. **No telemetry / no analytics.** Skills do not phone home. The bundle is private-first by design. The `fub-mcp-server` connects only to the realtor's own FUB account, with their own key.
5. **MIT-compatible deps only.** No GPL, no commercial-license libraries.

---

## Multi-harness compatibility (future)

The bundle ships for Claude Code + Cowork from Day 1. Codex, Cursor, and Gemini adapters land in `weeks 3-6`:

- `.codex-plugin/` — Codex plugin manifest
- `.cursor-plugin/` — Cursor plugin manifest
- `gemini-extension.json` — Gemini extension manifest

Skills should be written portably (use the SKILL.md standard); only the per-harness wrapper differs.

---

## Versioning

`VERSION` is the source of truth. CHANGELOG.md tracks user-visible changes per release. Bump `VERSION` AND the `plugin.json` `version` field together on every release.

- Pre-1.0: minor bumps (0.0.1 → 0.0.2 → 0.0.3) for additions; reserved for genuine breaking changes pre-launch
- Post-1.0: standard semver — patch / minor / major

---

## Do NOT

- Auto-send any message on a contact's behalf.
- Auto-deploy any FUB configuration without preview + approval.
- Generate "exclusive listing," "off-market," or "private listing" language unless the realtor has explicitly confirmed the listing has that status.
- Fabricate market data, neighborhood facts, or comparable sales.
- Embed CyclSales, Top Producer, or any other competing CRM lock-in. (Realty Stack is CRM-agnostic; Tier-2 is FUB-only because FUB is what the alpha cohort uses, not because of commercial coupling.)
- Ship a skill that violates an `ETHOS.md` rule. If you find a rule that's wrong, open an issue and propose a change before writing the skill.
