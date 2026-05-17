# v0.0.4 — Listing Presentation Skill Pair + /cma Retrofits — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.0.4 — two new skills (`/listing-presentation-template` + `/listing-presentation`) plus two cross-cutting retrofits to `/cma` (tab visibility upgrade + print CSS polish). New skills mirror the voice-draft / brand-kit-capture / cma patterns; retrofits make Cmd+P → PDF reliable across all visual outputs.

**Architecture:** The skill pair follows the build-once-fill-per-appointment pattern. `/listing-presentation-template` is a one-time consultative onboarding (Steps A–H, hybrid front-loaded data dump → analyze → propose → fill gaps → draft Email Voice → confirm → refine → save). `/listing-presentation` is per-appointment light personalization (Steps 1–5, optional inline `/cma` offer). Output is self-contained branded 4-tab HTML (Who I Am / How I Work / Track Record / Working Together). The retrofits document new Tab affordance + Print compatibility patterns in `output-style-guide.md` first, then apply across `/cma` seller, `/cma` buyer, and the new listing-presentation template.

**Tech Stack:** Markdown (SKILL.md, template files, style guide), HTML/CSS/JS (output templates), Bash (file ops), Python (no new scripts in v0.0.4). Same primitives as v0.0.3.

**Spec:** `docs/specs/2026-05-17-listing-presentation-design.md`

**Sibling skill prerequisites:** `voice-draft` (Email Voice for prose), `brand-kit-capture` (visual styling)

---

## File Structure

### To Create
- `skills/listing-presentation-template/SKILL.md` — consultative builder workflow (Steps A–H)
- `skills/listing-presentation/SKILL.md` — per-listing filler workflow (Steps 1–5)
- `skills/listing-presentation/references/html-template-listing-presentation.html` — 4-tab parameterized template, new tab affordance + print CSS from day 1
- `commands/listing-presentation-template.md` — slash command wrapper
- `commands/listing-presentation.md` — slash command wrapper

### To Modify
- `skills/cma/references/output-style-guide.md` — append "Tab affordance" + "Print compatibility" sections (canonical patterns documented first; everything else applies them)
- `skills/cma/references/html-template-seller.html` — replace tab CSS + tab markup + `@media print` block
- `skills/cma/references/html-template-buyer.html` — replace tab CSS + tab markup + `@media print` block (same retrofit shape as seller, smaller surface)
- `skills/using-realty-stack/SKILL.md` — add `/listing-presentation` to active catalog (`/listing-presentation-template` is one-time onboarding, not always-active)
- `skills/voice-draft/SKILL.md` — bump funnel hook footer v0.0.3 → v0.0.4
- `skills/brand-kit-capture/SKILL.md` — bump funnel hook footer
- `skills/using-realty-stack/SKILL.md` — bump funnel hook footer
- `skills/cma/SKILL.md` — bump funnel hook footer
- `.claude-plugin/plugin.json` — version bump
- `VERSION` — 0.0.3 → 0.0.4
- `README.md` — add new skills to table
- `CHANGELOG.md` — v0.0.4 entry

### Unchanged
- `skills/voice-draft/`, `skills/brand-kit-capture/`, `skills/cma/SKILL.md` body (only footers bumped)
- `skills/cma/scripts/`, `skills/cma/references/cma-methodology.md`, `skills/cma/references/research-prompts.md`
- `knowledge/` (voice-guide, constitution, fair-housing)
- `hooks/` (no SessionStart change — `/listing-presentation-template` is invoked by trigger phrase or `/listing-presentation` fallback, not auto-prompted)
- `CLAUDE.md` (no contract change — listing-presentation skills are consumers only of voice + brand contracts)
- `ETHOS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`

---

## Task 0: Update output-style-guide.md with canonical Tab affordance + Print compatibility patterns

**Files:**
- Modify: `skills/cma/references/output-style-guide.md` (append two new sections)

**Spec reference:** spec §"Design — Cross-cutting `/cma` retrofits" — Retrofit 1 (Tab affordance) and Retrofit 2 (Print CSS).

**Rationale:** These patterns get applied to three HTML templates (seller, buyer, listing-presentation). Documenting them in the style guide first means subsequent tasks reference the canonical block instead of re-deriving it.

- [ ] **Step 1: Read the current style guide**

Read `~/Claude/holden-alt/realty-stack/skills/cma/references/output-style-guide.md` end-to-end so the new sections match tone and structure.

- [ ] **Step 2: Append the Tab affordance section**

Use Edit to append the following section to the END of `output-style-guide.md` (after the final existing section, before the EOF):

```markdown

---

## 10. Tab affordance

**Problem the pattern solves.** Earlier `/cma` templates used a mono-caption tab label (`01 / OVERVIEW`) that reads as a page number, not a button. Sellers and buyers miss the tabs on first glance. The Tab affordance pattern keeps the editorial mono-caption styling while adding obvious button cues.

### CSS — canonical block

Paste this into every visual template's `<style>` block (replace the prior `.tab-btn` rules in `/cma` seller + buyer; new templates start with this from day 1):

```css
/* ============ TAB AFFORDANCE (v0.0.4 canonical) ============ */

nav.tabs {
  display: flex;
  gap: 6px;
  padding: 8px 0;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.tab-btn {
  appearance: none;
  background: var(--bg-deep);
  border: 1px solid var(--rule);
  border-radius: 6px;
  color: var(--ink-soft);
  font-family: var(--fm);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.tab-btn .tab-num {
  font-size: 9px;
  opacity: 0.6;
  font-weight: 400;
}

.tab-btn:hover {
  background: var(--ink-soft);
  color: var(--bg);
  border-color: var(--ink-soft);
}

.tab-btn:hover .tab-num { opacity: 0.85; }

.tab-btn.active {
  background: var(--ink);
  color: var(--bg);
  border-color: var(--ink);
}

.tab-btn.active .tab-num { color: var(--accent); opacity: 1; }

.tab-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.tab-panel { display: none; animation: fadeIn 0.3s ease; }
.tab-panel.active { display: block; }
```

### Markup — canonical pattern

```html
<nav class="tabs" role="tablist">
  <button class="tab-btn active" data-tab="overview" role="tab" aria-selected="true">
    <span class="tab-num">01</span> Overview
  </button>
  <button class="tab-btn" data-tab="cma" role="tab" aria-selected="false">
    <span class="tab-num">02</span> Comparables
  </button>
  <!-- additional tabs follow same shape -->
</nav>
```

### Mobile fallback

On viewports below 600px, retain the existing native `<select>` substitute. The Tab affordance pattern targets desktop / tablet; mobile keeps the `<select>` for thumb-friendliness. Don't try to scroll the desktop tab buttons horizontally on mobile — the `<select>` is more reliable.

### Design intent

- **Pigment discipline:** the accent color colors the `.tab-num` of the active tab only — single decorative element, no fill. Consistent with §2.
- **Active state contrast:** active tab inverts ink/bg for unambiguous selection. The brass on the tab number is the only accent pigment in the tab row.
- **Editorial preserved:** mono caption, uppercase, letter-spaced — keeps the brand voice; just adds a button shell so users know it's clickable.

---

## 11. Print compatibility

**Problem the pattern solves.** Realtors print their presentations to leave with sellers, and Cmd+P → Save as PDF is the path for emailed copies. Without explicit `@media print` rules, output has hidden tabs (only the active one prints), orphan content, visible interactive controls, and broken page breaks.

### CSS — canonical block

Paste this into every visual template's `<style>` block (replace the prior `@media print` block in `/cma` seller + buyer; new templates start with this from day 1):

```css
/* ============ PRINT COMPATIBILITY (v0.0.4 canonical) ============ */

@media print {
  /* Hide interactive controls */
  nav.tabs,
  .preset-chips,
  .reset-btn,
  button,
  input,
  select {
    display: none !important;
  }

  /* Expand all tabs simultaneously */
  .tab-panel {
    display: block !important;
    page-break-before: always;
  }
  .tab-panel:first-of-type {
    page-break-before: avoid;
  }

  /* Keep section cards together */
  .card,
  .comp-detail,
  .testimonial-card,
  .section-block {
    page-break-inside: avoid;
  }

  /* Preserve background colors where critical to design */
  .cover-hero,
  .accent-strip,
  .tab-num,
  .panel-caption {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Letter sizing — 0.5in margins via @page, body width clamp as fallback */
  body {
    font-family: var(--fd);
    max-width: 7.5in;
    margin: 0 auto;
    color: var(--ink);
    background: var(--bg);
  }

  @page {
    margin: 0.5in;
    size: letter;
  }

  /* Strip auto-appended URLs from links */
  a[href]::after { content: none; }
  a { color: var(--ink); text-decoration: none; }

  /* Typography legibility — bump body slightly for print */
  body { font-size: 11pt; line-height: 1.45; }
  h2 { font-size: 22pt; }
  h3 { font-size: 14pt; }
  h4 { font-size: 12pt; }
}
```

### Verification protocol

After applying this block to any template:

1. Open the generated HTML in Chrome.
2. Cmd+P → Destination: Save as PDF → preview pane.
3. Confirm: all tabs expand (every tab-panel content visible across pages), interactive controls hidden, each major tab section starts on a new page, cover hero retains background color, no auto-appended `(http://...)` after links.
4. Compare with Safari Cmd+P preview — confirm parity.

### Why these rules

- `display: none !important` for nav/buttons/inputs — printed copy is read, not interacted with.
- `page-break-before: always` on `.tab-panel` (except first) — each major section gets its own page; readers don't lose context across tabs.
- `page-break-inside: avoid` on cards — keeps an adjustment grid or testimonial intact instead of splitting mid-card.
- `-webkit-print-color-adjust: exact` — without this, Chrome strips background colors on print; the cover hero and accent strip go ghostly.
- `a[href]::after { content: none; }` — Chrome's default appends `(https://...)` to every link in print; this would clutter prose with URLs.
- `@page` size + margins — Letter with 0.5in margins matches what realtors expect when printing US-format material.
```

- [ ] **Step 3: Verify the file**

```bash
wc -l ~/Claude/holden-alt/realty-stack/skills/cma/references/output-style-guide.md
grep -c "^## " ~/Claude/holden-alt/realty-stack/skills/cma/references/output-style-guide.md
```
Expected: line count grew by ~150–180 (from the two new sections). H2 section count grew by 2 (now 11 H2s total).

- [ ] **Step 4: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/cma/references/output-style-guide.md
git commit -m "$(cat <<'EOF'
docs(cma): canonical Tab affordance + Print compatibility patterns

Adds §10 (Tab affordance) and §11 (Print compatibility) to output-style-guide.md
as the canonical patterns for every visual-output skill. Subsequent tasks apply
both blocks across /cma seller + buyer templates and the new listing-presentation
template (v0.0.4).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 1: Build the new HTML template for /listing-presentation

**Files:**
- Create: `skills/listing-presentation/references/html-template-listing-presentation.html`

**Spec reference:** spec §"Design — `/listing-presentation`" — Step 4 (HTML composition), placeholder list, cover hero composition.

**Pattern reference:** `~/Claude/holden-alt/realty-stack/skills/cma/references/html-template-seller.html` — copy structural conventions (Google Fonts link, CSS variables block, layout grid, mobile `<select>` fallback). Replace the 4-tab content with listing-presentation sections. Bake in the new Tab affordance + Print compatibility blocks from Task 0 from day 1.

**Required placeholders (exhaustive list — every one MUST appear in the template):**

Brand kit (same as /cma):
- `{{BG_COLOR}}`, `{{BG_DEEP_COLOR}}`, `{{INK_COLOR}}`, `{{INK_SOFT_COLOR}}`, `{{RULE_COLOR}}`, `{{ACCENT_COLOR}}`, `{{RED_COLOR}}`, `{{GREEN_COLOR}}`, `{{ACCENT_SOFT_COLOR}}`
- `{{GOOGLE_FONTS_LINK}}`, `{{DISPLAY_FONT}}`, `{{MONO_FONT}}`
- `{{WORDMARK_LEFT}}`, `{{WORDMARK_SEPARATOR}}`, `{{WORDMARK_RIGHT}}`
- `{{HEADSHOT_BASE64}}` (optional; surrounding markup degrades gracefully when empty — see Step 4)
- `{{LOGO_BASE64}}` (optional; same)

Per-listing:
- `{{SELLER_NAME}}`
- `{{PROPERTY_ADDRESS}}`
- `{{APPOINTMENT_DATE}}` (preformatted: "Tuesday, May 20, 2026")
- `{{CUSTOM_NOTE}}` (optional; surrounding `<p class="custom-note">` block omitted entirely if empty)

Agent profile (from voice profile):
- `{{AGENT_NAME}}`, `{{AGENT_BROKERAGE}}`, `{{AGENT_PRIMARY_MARKET}}`

Section content (from template file):
- `{{SECTION_LIST_TAB_1}}` — Who I Am
- `{{SECTION_LIST_TAB_2}}` — How I Work
- `{{SECTION_LIST_TAB_3}}` — Track Record
- `{{SECTION_LIST_TAB_4}}` — Working Together

Each `{{SECTION_LIST_TAB_N}}` expands to one or more `<section class="section-block">` blocks. Per-section sub-placeholders are rendered by the skill, not the template (the template treats SECTION_LIST_TAB_N as a single substituted HTML chunk).

Funnel hook footer (literal, hardcoded — not a placeholder):
- `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon`

- [ ] **Step 1: Read the seller template as structural model**

Read `~/Claude/holden-alt/realty-stack/skills/cma/references/html-template-seller.html` to understand: `<head>` structure, CSS variables block, layout grid, mobile select fallback, footer pattern.

- [ ] **Step 2: Read the new Tab affordance + Print compatibility blocks**

Read `~/Claude/holden-alt/realty-stack/skills/cma/references/output-style-guide.md` §10 and §11 — the EXACT CSS blocks from Task 0 are baked into this new template (not derived again).

- [ ] **Step 3: Write the new template**

Create `~/Claude/holden-alt/realty-stack/skills/listing-presentation/references/html-template-listing-presentation.html` with the structure below.

**Document structure (top to bottom):**

1. `<!DOCTYPE html><html lang="en"><head>` — meta, title (`Listing Presentation — {{SELLER_NAME}}`), Google Fonts link via `{{GOOGLE_FONTS_LINK}}`.
2. `<style>` block containing:
   - Leading comment with placeholder reference list
   - `:root` CSS variables (`--bg`, `--bg-deep`, `--ink`, `--ink-soft`, `--rule`, `--accent`, `--red`, `--green`, `--accent-soft`, `--fd`, `--fm`) populated from placeholders
   - Reset + base body styles (matches seller template)
   - Layout grid + container widths
   - Cover hero styles (split layout: wordmark left, optional headshot right, headline + address + date below)
   - **Tab affordance block — paste verbatim from output-style-guide.md §10**
   - Section block styles (`.section-block`, `.section-block h3`, prose styling)
   - Track Record table styles (recent listings grid)
   - Testimonial card styles (quote, attribution, optional photo)
   - Mobile responsive — native `<select>` fallback below 600px (mirror seller template)
   - **Print compatibility block — paste verbatim from output-style-guide.md §11**
3. `</head><body>` opens.
4. `<header class="cover-hero">` with:
   - Wordmark (CSS-rendered, three spans: `{{WORDMARK_LEFT}}{{WORDMARK_SEPARATOR}}{{WORDMARK_RIGHT}}`)
   - Optional headshot — if `{{HEADSHOT_BASE64}}` is non-empty, render `<img src="{{HEADSHOT_BASE64}}" alt="{{AGENT_NAME}}" class="agent-photo">`; otherwise omit the `<img>` entirely (do NOT render a broken/empty image tag)
   - H1: "Listing Presentation"
   - H2: "Prepared for {{SELLER_NAME}}"
   - `<p class="property-address">{{PROPERTY_ADDRESS}}</p>`
   - `<p class="appointment-date">{{APPOINTMENT_DATE}}</p>`
   - Optional custom note: if `{{CUSTOM_NOTE}}` is non-empty, render `<p class="custom-note">{{CUSTOM_NOTE}}</p>`; otherwise omit the `<p>` entirely
5. Mobile `<select>` (only visible on mobile via CSS, mirror seller pattern):
   ```html
   <select class="mobile-tabs" aria-label="Section navigation">
     <option value="who">Who I Am</option>
     <option value="how">How I Work</option>
     <option value="track">Track Record</option>
     <option value="working">Working Together</option>
   </select>
   ```
6. Desktop `<nav class="tabs" role="tablist">` with 4 tabs (Tab affordance markup pattern from §10):
   - `01 / Who I Am`
   - `02 / How I Work`
   - `03 / Track Record`
   - `04 / Working Together`
7. Four `<section class="tab-panel" id="...">` blocks, each containing:
   ```html
   <section class="tab-panel active" id="who">
     <div class="mono panel-caption">01 / WHO I AM</div>
     {{SECTION_LIST_TAB_1}}
   </section>
   <section class="tab-panel" id="how">
     <div class="mono panel-caption">02 / HOW I WORK</div>
     {{SECTION_LIST_TAB_2}}
   </section>
   <section class="tab-panel" id="track">
     <div class="mono panel-caption">03 / TRACK RECORD</div>
     {{SECTION_LIST_TAB_3}}
   </section>
   <section class="tab-panel" id="working">
     <div class="mono panel-caption">04 / WORKING TOGETHER</div>
     {{SECTION_LIST_TAB_4}}
   </section>
   ```
   First tab-panel has `active` class; others do not.
8. `<footer>` containing:
   - Agent name line: "{{AGENT_NAME}} · {{AGENT_BROKERAGE}}"
   - Optional logo (same conditional pattern as headshot — omit `<img>` entirely if `{{LOGO_BASE64}}` empty)
   - Funnel hook footer literal: `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon`
9. `<script>` block with tab-switching behavior:
   ```html
   <script>
     document.querySelectorAll('.tab-btn').forEach(btn => {
       btn.addEventListener('click', () => {
         const target = btn.dataset.tab;
         document.querySelectorAll('.tab-btn').forEach(b => {
           b.classList.toggle('active', b === btn);
           b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
         });
         document.querySelectorAll('.tab-panel').forEach(p => {
           p.classList.toggle('active', p.id === target);
         });
       });
     });
     // Mobile <select> mirrors tab state
     const sel = document.querySelector('.mobile-tabs');
     if (sel) {
       sel.addEventListener('change', () => {
         const target = sel.value;
         document.querySelectorAll('.tab-panel').forEach(p => {
           p.classList.toggle('active', p.id === target);
         });
       });
     }
   </script>
   ```
10. `</body></html>`.

**Conditional placeholder degradation:** for `{{HEADSHOT_BASE64}}`, `{{LOGO_BASE64}}`, `{{CUSTOM_NOTE}}` — the skill substitutes EMPTY STRING when the field is absent, and the template's surrounding markup must read sensibly with empty substitutions. The recommended approach: have the skill, not the template, emit the entire `<img>` / `<p class="custom-note">` block conditionally. The template uses a single placeholder like `{{COVER_HEADSHOT_HTML}}` that resolves to either a full `<img ...>` tag or empty string. Adjust the placeholder list above as needed — confirm with Holden in spec open-question #6 before finalizing.

- [ ] **Step 4: Verify the template renders standalone**

Write a tiny test substitution to confirm the template structure works. Create a temp shell test:

```bash
cd ~/Claude/holden-alt/realty-stack/skills/listing-presentation/references/
cp html-template-listing-presentation.html /tmp/lp-test.html

# Substitute minimal placeholders for a render test
sed -i.bak \
  -e 's/{{BG_COLOR}}/#F4F3EF/g' \
  -e 's/{{BG_DEEP_COLOR}}/#E8E6DF/g' \
  -e 's/{{INK_COLOR}}/#111418/g' \
  -e 's/{{INK_SOFT_COLOR}}/#3A3F46/g' \
  -e 's/{{RULE_COLOR}}/#C7C4BC/g' \
  -e 's/{{ACCENT_COLOR}}/#B08A44/g' \
  -e 's/{{ACCENT_SOFT_COLOR}}/#D4B373/g' \
  -e 's/{{RED_COLOR}}/#963c2a/g' \
  -e 's/{{GREEN_COLOR}}/#3d6b3d/g' \
  -e 's/{{DISPLAY_FONT}}/Inter/g' \
  -e 's/{{MONO_FONT}}/JetBrains Mono/g' \
  -e 's|{{GOOGLE_FONTS_LINK}}|<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700\&family=JetBrains+Mono:wght@400;500\&display=swap" rel="stylesheet">|g' \
  -e 's/{{WORDMARK_LEFT}}/Holden/g' \
  -e 's/{{WORDMARK_SEPARATOR}}/\//g' \
  -e 's/{{WORDMARK_RIGHT}}/GR/g' \
  -e 's/{{SELLER_NAME}}/Test Sellers/g' \
  -e 's/{{PROPERTY_ADDRESS}}/1247 Plainfield Ave NE, Grand Rapids MI/g' \
  -e 's/{{APPOINTMENT_DATE}}/Tuesday, May 20, 2026/g' \
  -e 's/{{AGENT_NAME}}/Holden Richardson/g' \
  -e 's/{{AGENT_BROKERAGE}}/RealSavvy/g' \
  -e 's/{{AGENT_PRIMARY_MARKET}}/Grand Rapids/g' \
  -e 's|{{CUSTOM_NOTE}}||g' \
  -e 's|{{HEADSHOT_BASE64}}||g' \
  -e 's|{{LOGO_BASE64}}||g' \
  -e 's|{{COVER_HEADSHOT_HTML}}||g' \
  -e 's|{{SECTION_LIST_TAB_1}}|<div class="section-block"><h3>About Me</h3><p>Placeholder About Me prose.</p></div>|g' \
  -e 's|{{SECTION_LIST_TAB_2}}|<div class="section-block"><h3>My Selling Process</h3><p>Placeholder process prose.</p></div>|g' \
  -e 's|{{SECTION_LIST_TAB_3}}|<div class="section-block"><h3>Recent Track Record</h3><p>Placeholder track record.</p></div>|g' \
  -e 's|{{SECTION_LIST_TAB_4}}|<div class="section-block"><h3>Fee Structure</h3><p>Placeholder fees.</p></div>|g' \
  /tmp/lp-test.html

open /tmp/lp-test.html
```
Expected: page opens in default browser; cover hero renders with wordmark + headline + seller name + address + date; 4 tabs visible with new Tab affordance styling; clicking each tab switches the panel; tab numbers have brass accent when active.

Then Cmd+P → Save as PDF preview:
Expected: all 4 tab panels visible across pages; no nav buttons in print; cover hero background preserved; no `(http://...)` after links.

Cleanup:
```bash
rm /tmp/lp-test.html /tmp/lp-test.html.bak
```

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/listing-presentation/references/html-template-listing-presentation.html
git commit -m "$(cat <<'EOF'
feat(listing-presentation): 4-tab parameterized HTML template

New visual-output template for /listing-presentation. Uses the canonical
Tab affordance + Print compatibility patterns from output-style-guide.md §10
and §11 from day 1. Cover hero composition: wordmark + optional headshot
+ headline + seller name + property address + appointment date + optional
custom note. Four tabs (Who I Am / How I Work / Track Record /
Working Together) each populated by a single SECTION_LIST_TAB_N placeholder
that the skill expands to one or more section-block elements.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Retrofit /cma seller HTML template (Tab affordance + Print CSS)

**Files:**
- Modify: `skills/cma/references/html-template-seller.html`

**Spec reference:** spec §"Retrofit 1 — Tab visibility upgrade" + §"Retrofit 2 — Print CSS polish".

**Pattern reference:** the canonical blocks in `output-style-guide.md` §10 and §11 (written in Task 0).

- [ ] **Step 1: Locate the existing tab CSS block**

```bash
grep -n "^.tab-btn\|^nav.tabs\|^.tab-panel\|@media print" ~/Claude/holden-alt/realty-stack/skills/cma/references/html-template-seller.html
```
Expected: shows the line ranges for the existing tab CSS (~lines 170–226), mobile tab CSS (~lines 1177–1193), and `@media print` block (~lines 1402–1404).

- [ ] **Step 2: Replace the existing tab CSS block**

Find this block in `html-template-seller.html` (starts around line 170, ends at the close of `.tab-panel.active { display: block; }` around line 226):

```css
nav.tabs {
  /* ... existing rules ... */
}
.tab-btn { /* ... */ }
.tab-btn .tab-num { /* ... */ }
.tab-btn:hover { color: var(--bg); }
.tab-btn:hover .tab-num { color: var(--metal); }
.tab-btn.active { /* ... */ }
.tab-btn.active .tab-num { color: var(--metal); }
/* etc */
.tab-panel { display: none; animation: fadeIn 0.3s ease; }
.tab-panel.active { display: block; }
```

Use Edit to replace the ENTIRE existing tab block (from `nav.tabs {` through `.tab-panel.active { display: block; }` inclusive) with the canonical Tab affordance block from `output-style-guide.md` §10 (paste verbatim).

**Important:** the canonical block uses `var(--rule)`, `var(--bg-deep)`, `var(--ink)`, `var(--ink-soft)`, `var(--bg)`, `var(--accent)`, `var(--fm)`. The seller template uses `--metal` for what is now `--accent` (legacy naming). Confirm via `grep -n "metal\|accent" html-template-seller.html`; if `--metal` is still in use elsewhere, leave it as-is for now (separate cleanup) — but the new Tab affordance block uses `--accent` exclusively, so map `--metal` → `--accent` ONLY inside the replacement Tab affordance CSS block, nowhere else.

- [ ] **Step 3: Replace the existing `@media print` block**

Find this block (starts around line 1402):

```css
@media print {
  nav.tabs, .preset-chips, .reset-btn { display: none; }
  .tab-panel { display: block !important; page-break-before: always; }
  .tab-panel:first-of-type { page-break-before: avoid; }
}
```

Use Edit to replace the ENTIRE existing `@media print` block (from `@media print {` through its closing `}`) with the canonical Print compatibility block from `output-style-guide.md` §11 (paste verbatim).

- [ ] **Step 4: Update the tab markup if needed**

Find the existing nav block (around line 1425):
```html
<nav class="tabs">
  <button class="tab-btn active" data-tab="overview"><span class="tab-num">01</span> Overview</button>
  <button class="tab-btn" data-tab="cma"><span class="tab-num">02</span> Comparables</button>
  <button class="tab-btn" data-tab="netsheet"><span class="tab-num">03</span> Net Sheet</button>
  <button class="tab-btn" data-tab="marketing"><span class="tab-num">04</span> Marketing</button>
</nav>
```

Use Edit to add `role="tablist"` to the `<nav class="tabs">` opening tag, and `role="tab"` + `aria-selected` to each button (matches canonical markup pattern from §10). Final markup:

```html
<nav class="tabs" role="tablist">
  <button class="tab-btn active" data-tab="overview" role="tab" aria-selected="true"><span class="tab-num">01</span> Overview</button>
  <button class="tab-btn" data-tab="cma" role="tab" aria-selected="false"><span class="tab-num">02</span> Comparables</button>
  <button class="tab-btn" data-tab="netsheet" role="tab" aria-selected="false"><span class="tab-num">03</span> Net Sheet</button>
  <button class="tab-btn" data-tab="marketing" role="tab" aria-selected="false"><span class="tab-num">04</span> Marketing</button>
</nav>
```

If the existing tab-switching JS doesn't already toggle `aria-selected`, update it:
```js
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => {
      b.classList.toggle('active', b === btn);
      b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
    });
    document.querySelectorAll('.tab-panel').forEach(p => {
      p.classList.toggle('active', p.id === target);
    });
  });
});
```

- [ ] **Step 5: Verify visually**

```bash
cd ~/Claude/holden-alt/realty-stack/skills/cma/references/
cp html-template-seller.html /tmp/cma-seller-test.html

# Substitute minimal placeholders (use the same sed block as Task 1 Step 4, plus
# any seller-specific placeholders like {{SUBJECT_ADDRESS}}, {{COMP_LIST_HTML}}
# substituted to "TEST" so the template renders something).
# Use a small substitution script — sed for the brand kit placeholders only is
# sufficient to confirm the tab + print CSS works; complex placeholders can
# stay literal in the test render.

open /tmp/cma-seller-test.html
```
Expected: tabs render with the new button-style affordance, distinct active state, brass accent on the active tab number. Cmd+P preview shows all 4 tab panels expanded across pages with no nav buttons visible.

Cleanup:
```bash
rm /tmp/cma-seller-test.html
```

- [ ] **Step 6: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/cma/references/html-template-seller.html
git commit -m "$(cat <<'EOF'
fix(cma): apply v0.0.4 Tab affordance + Print CSS to seller template

Retrofits the seller listing presentation template with the canonical
Tab affordance (button-shaped tabs with distinct active state, brass accent
on active tab-num) and Print compatibility (expand all tabs on print, hide
interactive controls, preserve background colors, strip auto-URLs).
Markup gains ARIA roles. Print output now produces clean PDFs via Cmd+P.

Refs: docs/specs/2026-05-17-listing-presentation-design.md §"Retrofit 1"
and §"Retrofit 2".

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Retrofit /cma buyer HTML template (Tab affordance + Print CSS)

**Files:**
- Modify: `skills/cma/references/html-template-buyer.html`

Same retrofit shape as Task 2, smaller surface (3 tabs instead of 4: Scenarios / Math / Mortgage Calculator).

- [ ] **Step 1: Locate the existing tab + print blocks**

```bash
grep -n "^.tab-btn\|^nav.tabs\|^.tab-panel\|@media print" ~/Claude/holden-alt/realty-stack/skills/cma/references/html-template-buyer.html
```

- [ ] **Step 2: Replace the existing tab CSS block**

Same operation as Task 2 Step 2 — find the existing tab CSS block (`nav.tabs` through `.tab-panel.active`) and replace verbatim with the canonical Tab affordance block from `output-style-guide.md` §10.

- [ ] **Step 3: Replace the existing `@media print` block**

Same operation as Task 2 Step 3 — find the existing `@media print` block and replace verbatim with the canonical Print compatibility block from `output-style-guide.md` §11.

- [ ] **Step 4: Update the tab markup**

Same operation as Task 2 Step 4 — add `role="tablist"` to `<nav class="tabs">`, add `role="tab"` + `aria-selected` to each `<button>`. The buyer template has 3 tabs (Scenarios / Math / Mortgage Calc):

```html
<nav class="tabs" role="tablist">
  <button class="tab-btn active" data-tab="scenarios" role="tab" aria-selected="true"><span class="tab-num">01</span> Scenarios</button>
  <button class="tab-btn" data-tab="math" role="tab" aria-selected="false"><span class="tab-num">02</span> Math</button>
  <button class="tab-btn" data-tab="mortgage" role="tab" aria-selected="false"><span class="tab-num">03</span> Mortgage Calculator</button>
</nav>
```

Update the JS to toggle `aria-selected` if not already doing so (same code block as Task 2).

- [ ] **Step 5: Verify visually**

Same sed-substitution test as Task 2 Step 5, with buyer-specific placeholders set to literal "TEST" where needed. Cmd+P preview should show all 3 tab panels expanded.

- [ ] **Step 6: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/cma/references/html-template-buyer.html
git commit -m "$(cat <<'EOF'
fix(cma): apply v0.0.4 Tab affordance + Print CSS to buyer template

Mirrors the seller-template retrofit for the 3-tab buyer offer strategy
template. Same canonical Tab affordance + Print compatibility blocks from
output-style-guide.md §10 and §11; ARIA roles added.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Write skills/listing-presentation-template/SKILL.md

**Files:**
- Create: `skills/listing-presentation-template/SKILL.md`

**Spec reference:** `docs/specs/2026-05-17-listing-presentation-design.md` §"Design — `/listing-presentation-template`" — Steps A–H.

**Requirements (all MUST be present):**

1. **Frontmatter (exact):**

```yaml
---
name: listing-presentation-template
description: This skill should be used when a real estate agent asks to "set up my listing presentation", "build my listing pitch", "create my listing presentation template", "I want a listing presentation", "configure my listing template", or "build my listing presentation template". One-time consultative builder that captures the agent's reusable listing-presentation content (about-me, process, marketing philosophy, track record, testimonials, pricing, fees) and persists to ~/.config/realty-stack/listing-presentation-template.md so per-listing /listing-presentation can render in seconds.
version: 0.0.1
---
```

2. **Body sections (in order):**

- **H1:** `# Listing Presentation Template — Build Once, Fill Per Appointment`
- Brief intro (≤3 sentences): one-time consultative onboarding; captures reusable pitch content; sibling to `/cma` (this is about the agent, that is per-property analytics).
- **"When this skill runs"** — list trigger phrases verbatim from the frontmatter description, plus the inline fallback when `/listing-presentation` is invoked without a template.
- **"Voice profile + brand kit pre-checks"** — verify both pre-requisites; run `voice-draft` / `brand-kit-capture` inline if missing (mirror /cma's pattern).
- **"Onboarding workflow"** — Steps A through H per the spec. Each step section MUST include:
  - The exact realtor-facing question/copy verbatim from the spec where present
  - The 8 standard sections list verbatim (About Me / Why Hire Me / My Selling Process / Marketing Philosophy / Recent Track Record / Testimonials / Pricing Philosophy / Fee Structure)
  - Sub-question lists for Step D verbatim per spec
  - Compliance discipline for Step E verbatim (no fair housing red flags, no "guaranteed", no fabricated stats, Pricing = general, Marketing = vague/phase-based)
  - Approval phrases for Step G: "ship it" / "approved" / "save it" / "good enough" / "OK as-is" / "done" / "perfect"
  - Step H file-write protocol: Bash `mkdir -p ~/.config/realty-stack/`, then Write the markdown template
  - Confirmation copy verbatim: *"Saved to ~/.config/realty-stack/listing-presentation-template.md. Run /listing-presentation any time you have a listing appointment — it'll fill the template for that specific seller and property."*
- **"Template file format"** — the full markdown structure from the spec §"Template file format". Include the optional `headshot_override` field. Include the example.
- **"Existing template detection at Step A"** — three-path flow: update specific sections / start fresh / cancel. Update mode = re-runs Steps E–G for selected sections only. Fresh = builds from scratch (overwrites on Step H approval). Cancel = exit.
- **"Section-to-tab mapping"** — explicit mapping of the 8 standard sections to the 4 output tabs:
  - Tab 1 "Who I Am" = About Me, Why Hire Me
  - Tab 2 "How I Work" = My Selling Process, Marketing Philosophy
  - Tab 3 "Track Record" = Recent Track Record, Testimonials
  - Tab 4 "Working Together" = Pricing Philosophy, Fee Structure
- **"Custom section handling"** — when the agent adds a section beyond the 8, skill classifies the section's theme against the 4 tab themes and proposes a tab; agent confirms.
- **"Edge cases"** — the full table from the spec §"Edge cases & failure modes (template builder)"
- **"What this skill never does"** — distilled from spec §"What these skills never do":
  - Fabricate stats, awards, or testimonials
  - Persist anything to voice-profile.md or brand-kit.md
  - Skip the compliance check on testimonials
  - Save before Step H approval
  - Auto-edit testimonials with protected-class language (flag and ask)
  - Mix Text Voice with Email Voice
- **Funnel hook footer (literal text):** `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon`

3. **Writing style:** imperative/infinitive form throughout the body. Third-person in frontmatter description. Lean (~300 lines target — push detail to references if it grows beyond that).

4. **Length budget:** SKILL.md body 300 lines max per CLAUDE.md project rule. If it grows beyond, extract a `references/section-drafting-guide.md` with the Step E compliance discipline + section-specific prose guidance.

- [ ] **Step 1: Read the spec for full context**

Read `~/Claude/holden-alt/realty-stack/docs/specs/2026-05-17-listing-presentation-design.md` §"Design — `/listing-presentation-template`" end-to-end.

- [ ] **Step 2: Read brand-kit-capture/SKILL.md as pattern reference**

Read `~/Claude/holden-alt/realty-stack/skills/brand-kit-capture/SKILL.md` — closest pattern (consultative onboarding with Steps A–I). Match its tone, structure, and edge-case table format.

- [ ] **Step 3: Write the SKILL.md**

Create `~/Claude/holden-alt/realty-stack/skills/listing-presentation-template/SKILL.md` with all requirements above. Length target: ~300 lines.

- [ ] **Step 4: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/listing-presentation-template/SKILL.md
git commit -m "$(cat <<'EOF'
feat: listing-presentation-template skill — consultative builder

One-time onboarding that captures the agent's reusable listing-presentation
content via hybrid front-loaded data dump (Step A) → categorize into 8
standard sections (Step B) → propose structure + flag gaps (Step C) →
targeted gap-fill questions (Step D) → draft each section in Email Voice
(Step E) → confirmation (Step F) → refinement loop (Step G) →
write template file (Step H). Persists to
~/.config/realty-stack/listing-presentation-template.md.

Required by /listing-presentation (next task). Mirrors voice-draft +
brand-kit-capture pattern.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Write skills/listing-presentation/SKILL.md

**Files:**
- Create: `skills/listing-presentation/SKILL.md`

**Spec reference:** `docs/specs/2026-05-17-listing-presentation-design.md` §"Design — `/listing-presentation`" — Steps 1–5.

**Requirements (all MUST be present):**

1. **Frontmatter (exact):**

```yaml
---
name: listing-presentation
description: This skill should be used when a real estate agent asks to "make a listing presentation for [address]", "listing presentation for [seller]", "I have a listing appointment with [address]", "prepare for my listing appointment", "build my pitch for [address]", or "create my listing presentation for [seller]". Per-listing skill that loads the agent's saved template, asks for light personalization (seller name, property address, appointment date, optional custom note), and produces a self-contained branded 4-tab HTML pitch. Offers to also run /cma inline at Step 3 for one-appointment-two-artifacts.
version: 0.0.1
---
```

2. **Body sections (in order):**

- **H1:** `# Listing Presentation — Per-Appointment Pitch`
- Brief intro (≤3 sentences): per-listing fill of the saved template + light personalization; sibling to `/cma`; optional `/cma` chain at Step 3.
- **"When this skill runs"** — trigger phrases verbatim from the frontmatter description.
- **"Path fork — overlap with /cma"** — handles trigger ambiguity. Copy verbatim from spec §"Path fork":
  > *"Want the listing pitch (the about-you / process / track-record piece) or the CMA (the numbers — what to price at)? Or both? Both = two artifacts at the same appointment."*
- **"Pre-checks"** — voice profile, brand kit, template. Template fallback: if missing, run `/listing-presentation-template` inline to completion before continuing.
- **"Per-listing workflow"** — Steps 1 through 5 per the spec:
  - Step 1 question copy verbatim
  - Step 2 confirmation copy verbatim
  - Step 3 /cma offer copy verbatim: *"Want me to also run /cma for this property?"*
  - Step 4 HTML build — load `references/html-template-listing-presentation.html`, substitute every `{{PLACEHOLDER}}`. Brand kit substitution list. Asset embedding rules. Per-listing personalization placeholders. Section content placeholders ({{SECTION_LIST_TAB_1}} through {{SECTION_LIST_TAB_4}}) — each is a single HTML chunk the skill builds from the template's section list, grouped by tab assignment.
  - Step 5 file-write protocol: default path `~/Downloads/<property-slug>-listing-presentation.html`; path conflict appends timestamp suffix; override honored.
  - Confirmation copy verbatim: *"Saved to ~/Downloads/{slug}-listing-presentation.html — open in Chrome / Safari to preview, ⌘P prints cleanly with all tabs expanded."*
- **"Section rendering — how SECTION_LIST_TAB_N is built"** — for each tab, iterate the template's sections assigned to that tab, emit one `<section class="section-block">` per template section. Section block structure:
  ```html
  <section class="section-block">
    <h3>{{section_title}}</h3>
    <div class="section-content">
      {{section_prose}}
    </div>
    <!-- structured content for specific section types: -->
    <!-- Recent Track Record: table of past listings -->
    <!-- Testimonials: card list with optional photos (base64-embedded) -->
  </section>
  ```
- **"Cover hero composition"** — wordmark + optional headshot (brand kit or template override) + "Listing Presentation" + "Prepared for {{SELLER_NAME}}" + property address + appointment date + optional custom note. Match the spec.
- **"Voice profile use at per-listing generation"** — template prose is already in Email Voice (drafted at template build). Per-listing skill drafts ONLY the cover greeting framing (e.g., personalization of the custom note intro) in Email Voice. Don't re-draft template sections.
- **"Testimonial photo handling at generation"** — read photo file, base64-encode, embed inline. If path missing at generation: skip silently (text-only quote rendered).
- **"Optional inline /cma offer (Step 3)"** — workflow: ask once → if yes, run /cma inline (full /cma flow — seller path) → outputs land in ~/Downloads/ as two files → return to Step 4 to finish listing-presentation file.
- **"Edge cases"** — the full table from spec §"Edge cases & failure modes (per-listing)"
- **"What this skill never does"** — distilled:
  - Re-draft template prose per listing (template prose is canonical)
  - Render `<img>` tags with empty `src` attributes (omit the tag entirely if asset missing)
  - Reference asset files by path in output HTML (always base64-embed)
  - Use a default brand or anyone else's brand (always active brand kit)
  - Overwrite output files silently (timestamp suffix on conflict)
  - Save without explicit per-listing personalization (Step 1 inputs required)
- **Funnel hook footer (literal):** `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon`

3. **Writing style:** imperative/infinitive form throughout body. Third-person in frontmatter description. Lean (~250 lines target).

4. **Length budget:** SKILL.md body 300 lines max per CLAUDE.md project rule.

- [ ] **Step 1: Read the spec for full context**

Read `~/Claude/holden-alt/realty-stack/docs/specs/2026-05-17-listing-presentation-design.md` §"Design — `/listing-presentation`" end-to-end.

- [ ] **Step 2: Read /cma SKILL.md as pattern reference**

Read `~/Claude/holden-alt/realty-stack/skills/cma/SKILL.md` — closest pattern (per-invocation skill with HTML output). Match its tone, structure, edge-case table format. Pay attention to the Step 8 file-write protocol and the placeholder substitution discipline.

- [ ] **Step 3: Write the SKILL.md**

Create `~/Claude/holden-alt/realty-stack/skills/listing-presentation/SKILL.md` with all requirements above. Length target: ~250 lines.

- [ ] **Step 4: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/listing-presentation/SKILL.md
git commit -m "$(cat <<'EOF'
feat: listing-presentation skill — per-appointment HTML pitch generator

Per-listing skill that loads the agent's saved template
(~/.config/realty-stack/listing-presentation-template.md) plus light
personalization (seller name, property address, appointment date,
optional custom note) and produces a self-contained branded 4-tab HTML
pitch via references/html-template-listing-presentation.html. Optional
inline /cma offer at Step 3 lets the agent generate both artifacts in
one flow. Mirrors /cma's per-invocation pattern; reuses the same
brand-kit + voice-profile overlay loads.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Create slash command wrappers for both new skills

**Files:**
- Create: `commands/listing-presentation-template.md`
- Create: `commands/listing-presentation.md`

**Pattern reference:** existing `commands/cma.md` — slim wrappers that reference the skill by name.

- [ ] **Step 1: Read the existing /cma command wrapper**

Read `~/Claude/holden-alt/realty-stack/commands/cma.md` to confirm the wrapper format. Expected: short markdown file with frontmatter listing the skill name + a brief instruction to invoke the skill.

- [ ] **Step 2: Create commands/listing-presentation-template.md**

Use Write to create `~/Claude/holden-alt/realty-stack/commands/listing-presentation-template.md` matching the cma.md wrapper pattern:

```markdown
---
name: listing-presentation-template
description: Build the agent's reusable listing-presentation template (one-time consultative onboarding).
---

Invoke the `listing-presentation-template` skill to walk the agent through building their reusable listing-presentation content. Hybrid front-loaded data dump → categorize into 8 standard sections → propose structure → fill gaps → draft Email Voice → confirm → refine → save to `~/.config/realty-stack/listing-presentation-template.md`.

See `skills/listing-presentation-template/SKILL.md` for the full workflow.
```

- [ ] **Step 3: Create commands/listing-presentation.md**

Use Write to create `~/Claude/holden-alt/realty-stack/commands/listing-presentation.md`:

```markdown
---
name: listing-presentation
description: Generate a per-appointment 4-tab HTML listing presentation from the saved template + light personalization.
---

Invoke the `listing-presentation` skill to produce a branded 4-tab HTML listing presentation for a specific seller and property. Loads the saved template at `~/.config/realty-stack/listing-presentation-template.md`, asks for seller name + address + appointment date + optional custom note, and writes the file to `~/Downloads/`. Optional inline /cma offer at Step 3.

If no template exists, the skill runs `listing-presentation-template` inline first.

See `skills/listing-presentation/SKILL.md` for the full workflow.
```

- [ ] **Step 4: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add commands/listing-presentation-template.md commands/listing-presentation.md
git commit -m "$(cat <<'EOF'
feat: slash command wrappers for listing-presentation skill pair

Adds /listing-presentation-template and /listing-presentation slash command
wrappers. Both delegate to the corresponding skills under skills/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Update using-realty-stack overlay catalog

**Files:**
- Modify: `skills/using-realty-stack/SKILL.md`

**Goal:** add `/listing-presentation` to the active skill catalog so the overlay can route trigger phrases. `/listing-presentation-template` is NOT added (one-time onboarding skill, invoked by trigger phrase or by /listing-presentation fallback, not always-active routing).

- [ ] **Step 1: Read current overlay**

Read `~/Claude/holden-alt/realty-stack/skills/using-realty-stack/SKILL.md` to locate the "active skill catalog" / "skills available in this session" section (whatever name v0.0.3 used for the routing table).

- [ ] **Step 2: Add the /listing-presentation entry**

Use Edit to insert a new catalog entry after the existing `/cma` entry. Match the catalog format (whatever shape the existing entries use). The entry's content:

- **Slash command:** `/listing-presentation`
- **Purpose:** Per-appointment 4-tab HTML pitch from saved template + light personalization
- **Trigger phrases:** "make a listing presentation for", "listing presentation for", "I have a listing appointment with", "prepare for my listing appointment", "build my pitch for", "create my listing presentation"
- **Pre-requisites:** voice profile, brand kit, listing-presentation template (auto-onboarding if missing)
- **Optional chain:** Step 3 offers inline /cma run for one-appointment-two-artifacts

- [ ] **Step 3: Validate**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 4: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add skills/using-realty-stack/SKILL.md
git commit -m "$(cat <<'EOF'
feat: add /listing-presentation to overlay catalog

Adds /listing-presentation to the active skill catalog so the overlay
routes trigger phrases. /listing-presentation-template is intentionally
omitted — it's one-time onboarding invoked by trigger phrase or by
/listing-presentation's inline fallback, not always-active routing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Bump VERSION + plugin.json + funnel hook footers

**Files:**
- Modify: `VERSION`
- Modify: `.claude-plugin/plugin.json`
- Modify: `skills/voice-draft/SKILL.md` (footer line only)
- Modify: `skills/brand-kit-capture/SKILL.md` (footer line only)
- Modify: `skills/using-realty-stack/SKILL.md` (footer line only)
- Modify: `skills/cma/SKILL.md` (footer line only)

New skills (`listing-presentation-template`, `listing-presentation`) are born at v0.0.4 — their footers don't need updating.

- [ ] **Step 1: Bump VERSION**

```bash
echo "0.0.4" > ~/Claude/holden-alt/realty-stack/VERSION
cat ~/Claude/holden-alt/realty-stack/VERSION
```
Expected: `0.0.4`

- [ ] **Step 2: Bump plugin.json version**

Read `~/Claude/holden-alt/realty-stack/.claude-plugin/plugin.json`. Use Edit to change the `"version"` field from `"0.0.3"` to `"0.0.4"`. Leave the rest of the manifest unchanged.

Verify:
```bash
grep '"version"' ~/Claude/holden-alt/realty-stack/.claude-plugin/plugin.json
```
Expected: `"version": "0.0.4",`

- [ ] **Step 3: Bump funnel hook footers across existing skills**

For each of the 4 existing skill files (voice-draft, brand-kit-capture, using-realty-stack, cma), the footer is the last line:

Before: `✨ Realty Stack v0.0.3 — Realty Brain (FUB-powered always-on AI) coming soon`
After:  `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon`

Use Edit on each file to replace `v0.0.3` with `v0.0.4` in that footer line only.

Verify all four files updated:
```bash
grep -l "Realty Stack v0.0.4" ~/Claude/holden-alt/realty-stack/skills/*/SKILL.md
```
Expected: 6 files (voice-draft, brand-kit-capture, using-realty-stack, cma, listing-presentation-template, listing-presentation).

```bash
grep "Realty Stack v0.0.3" ~/Claude/holden-alt/realty-stack/skills/*/SKILL.md
```
Expected: no output (no remaining v0.0.3 footers).

- [ ] **Step 4: Validate the plugin**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed."

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add VERSION .claude-plugin/plugin.json skills/voice-draft/SKILL.md skills/brand-kit-capture/SKILL.md skills/using-realty-stack/SKILL.md skills/cma/SKILL.md
git commit -m "$(cat <<'EOF'
chore: bump to v0.0.4 + sync funnel hook footers

VERSION, .claude-plugin/plugin.json, and the funnel hook footers across
all four existing skills (voice-draft, brand-kit-capture,
using-realty-stack, cma) bumped v0.0.3 → v0.0.4. The two new skills
shipped this cycle (listing-presentation-template, listing-presentation)
are born at v0.0.4 and don't need bumping.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Update README + CHANGELOG for v0.0.4

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Read current README + CHANGELOG**

Read `~/Claude/holden-alt/realty-stack/README.md` (locate the skills table) and `~/Claude/holden-alt/realty-stack/CHANGELOG.md` (locate the top of the entries — newest first).

- [ ] **Step 2: Update README skills table**

Use Edit to add two new rows to the skills table — one for each new skill. Match the existing table column structure. Suggested entries:

| Skill | Trigger | What it does |
|---|---|---|
| `/listing-presentation-template` | "set up my listing presentation", "build my listing pitch" | One-time consultative builder for the agent's reusable listing-presentation content. Saves to `~/.config/realty-stack/listing-presentation-template.md`. |
| `/listing-presentation` | "make a listing presentation for [address]", "I have a listing appointment with [address]" | Per-appointment 4-tab HTML pitch from saved template + light personalization. Optional inline `/cma` chain. |

(Adapt the column shape to whatever the existing table uses.)

- [ ] **Step 3: Update CHANGELOG.md**

Use Edit to insert a new top entry above the existing v0.0.3 entry:

```markdown
## v0.0.4 — 2026-05-17

### New skills
- **`/listing-presentation-template`** — one-time consultative builder that captures the agent's reusable listing-presentation content (about-me, process, marketing philosophy, track record, testimonials, pricing, fees). Hybrid front-loaded data-dump pattern. Persists to `~/.config/realty-stack/listing-presentation-template.md`. Sibling to `voice-draft` + `brand-kit-capture` — paid once in time, every appointment after benefits.
- **`/listing-presentation`** — per-appointment skill that loads the saved template plus light personalization (seller name, address, appointment date, optional custom note) and produces a self-contained branded 4-tab HTML pitch (Who I Am / How I Work / Track Record / Working Together). Optional inline `/cma` offer at Step 3 — one appointment, both artifacts.

### Cross-cutting visual improvements (apply to all visual-output templates)
- **Tab affordance upgrade.** Tabs now render as buttons with clear active state instead of the v0.0.3 mono-caption labels that read as page numbers. Applied to `/cma` seller, `/cma` buyer, and the new `/listing-presentation` template. Canonical pattern documented in `skills/cma/references/output-style-guide.md` §10.
- **Print CSS polish.** Cmd+P → Save as PDF now produces clean output across all visual templates: all tabs expanded, interactive controls hidden, backgrounds preserved, no auto-appended URLs. Canonical pattern documented in `skills/cma/references/output-style-guide.md` §11.

### Other
- `output-style-guide.md` gains §10 (Tab affordance) and §11 (Print compatibility) as canonical patterns for every future visual-output skill.
- Funnel hook footers synced across all skills to `v0.0.4`.
```

- [ ] **Step 4: Verify**

```bash
head -50 ~/Claude/holden-alt/realty-stack/CHANGELOG.md
grep -c "listing-presentation" ~/Claude/holden-alt/realty-stack/README.md
```
Expected: CHANGELOG opens with the new v0.0.4 block; README grep returns ≥2 (both new skill rows present).

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/holden-alt/realty-stack
git add README.md CHANGELOG.md
git commit -m "$(cat <<'EOF'
docs: v0.0.4 README skills table + CHANGELOG entry

README skills table gains rows for /listing-presentation-template and
/listing-presentation. CHANGELOG documents both new skills, the
cross-cutting Tab affordance + Print CSS retrofits to /cma, and the
new output-style-guide.md §10/§11 canonical patterns.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Plugin reinstall + smoke test

**Files:** None modified; verification only.

- [ ] **Step 1: Final plugin validation**

```bash
claude plugin validate ~/Claude/holden-alt/realty-stack
```
Expected: "Validation passed." No errors, no warnings.

- [ ] **Step 2: Reinstall locally**

```bash
claude plugin uninstall realty-stack
claude plugin marketplace update realty-stack
claude plugin install realty-stack@realty-stack
claude plugin details realty-stack
```
Expected:
- Plugin version shows `0.0.4`
- Skills (6): `voice-draft`, `brand-kit-capture`, `using-realty-stack`, `cma`, `listing-presentation-template`, `listing-presentation`
- Commands (3): `cma`, `listing-presentation-template`, `listing-presentation`
- Hooks (1): SessionStart

- [ ] **Step 3: Smoke-test skill routing**

Open a fresh Claude Code session in any directory:

```bash
cd /tmp && claude
```

In Claude Code, type each of these prompts (one at a time, in isolation):

1. *"Set up my listing presentation"* → Should route to `listing-presentation-template`.
2. *"Make a listing presentation for 1247 Plainfield"* → Should route to `listing-presentation`.
3. *"Run a CMA on 1247 Plainfield"* → Should still route to `/cma` (regression check).

For each: verify Claude's first response references the right skill. No actual work needed — just confirm routing fires. Cancel each session after the routing confirmation.

- [ ] **Step 4: No commit (verification only)**

If Steps 1–3 all pass, proceed to Task 11. If any fail, fix the issue (likely a frontmatter description tweak or a trigger phrase miss) and re-test.

---

## Task 11: Human-in-loop end-to-end test

**Files:** None modified; verification only.

Holden builds his actual listing-presentation template using the consultative flow, generates a presentation for a hypothetical seller, and verifies HTML + PDF output quality. Per CLAUDE.md project rule: "Every new skill MUST be tested on Holden's real work before commit."

- [ ] **Step 1: Clean state for the template**

```bash
rm -f ~/.config/realty-stack/listing-presentation-template.md
```
Do NOT touch voice-profile.md or brand-kit.md — both must remain.

- [ ] **Step 2: Holden opens a fresh Claude Code session**

```bash
cd ~/Claude/holden-alt/realty-stack
claude
```

- [ ] **Step 3: Run `/listing-presentation-template`**

Holden prompts: *"Set up my listing presentation."*

Walk through Steps A–H with Holden's real material:
- Step A: Holden pastes / describes whatever he has — past presentations, bio (Holden/GR), brokerage profile (RealSavvy), testimonials from real clients, sample past listings, his real headshot path, any awards / certifications
- Steps B–C: skill categorizes + proposes structure; Holden confirms
- Step D: skill asks targeted gap questions; Holden answers
- Step E: skill drafts each section in Email Voice; Holden reads
- Step F: full draft shown
- Step G: Holden refines as needed (real freeform feedback)
- Step H: approved + saved

Verify the template file:
```bash
cat ~/.config/realty-stack/listing-presentation-template.md
```
Expected: all sections present, prose sounds like Holden's voice, no fair housing red flags, no fabricated stats, tab assignments valid.

- [ ] **Step 4: Run `/listing-presentation` for a hypothetical seller**

In the same session, Holden prompts: *"Make a listing presentation for the Smiths at 1247 Plainfield Ave NE, appointment Tuesday May 20."*

Walk through Steps 1–5:
- Step 1: seller "Smith family", address "1247 Plainfield Ave NE", date "Tuesday, May 20, 2026", optional custom note (Holden's call)
- Step 2: confirms template freshness
- Step 3: skill asks about inline /cma — Holden's call (test both branches across multiple test runs if time)
- Step 4: HTML built
- Step 5: file written to `~/Downloads/1247-plainfield-ave-ne-listing-presentation.html`

- [ ] **Step 5: Verify the HTML output**

```bash
open ~/Downloads/1247-plainfield-ave-ne-listing-presentation.html
```

Visual checks in Chrome:
- Cover hero renders: wordmark + (headshot, if present) + "Listing Presentation" + "Prepared for the Smith family" + address + date + (custom note, if provided)
- 4 tabs visible with new Tab affordance (button-shaped, brass accent on active tab-num, distinct active state)
- Clicking each tab switches the panel
- Each section's prose reads in Holden's voice
- Brand colors are Holden's brand kit values (limestone bg, brass accents, etc.)
- Wordmark renders as CSS text (sharp at any zoom)
- Mobile: shrink Chrome window below 600px → `<select>` appears, desktop tab nav hides

Visual checks in Safari (parity):
- Same render in Safari
- Mobile Safari render via Cmd+Option+R Responsive Design Mode → iPhone preset → `<select>` works

- [ ] **Step 6: Verify the print output**

In Chrome with the HTML open: Cmd+P → Destination: Save as PDF → Preview pane.

Checks:
- All 4 tab panels visible across pages (every section content present)
- No nav buttons / interactive controls visible
- Each major tab section starts on a new page
- Cover hero background color preserved
- No auto-appended `(http://...)` after links

Save the PDF and open in Preview for a final eyeball.

Same Cmd+P test in Safari for parity.

- [ ] **Step 7: Sanity-check no regressions in /cma**

Holden quickly runs `/cma` on the same hypothetical address to confirm the Tab affordance + Print CSS retrofits didn't break /cma output. Open the resulting HTML in Chrome, click each tab, Cmd+P preview.

- [ ] **Step 8: Note any issues found**

If the e2e surfaced bugs (typos, missing trigger phrases, missing edge cases, render glitches), commit fixes. Otherwise no commit needed — verification only.

---

## Task 12: GitHub push v0.0.4 (gated)

**Files:** None modified; push only.

**Standing rule:** explicit approval gate per Holden's standing rule. Do NOT push v0.0.4 without Holden's explicit "ship it" / "push" / "release" approval in this session.

- [ ] **Step 1: Confirm working tree is clean**

```bash
cd ~/Claude/holden-alt/realty-stack
git status
```
Expected: "nothing to commit, working tree clean".

- [ ] **Step 2: Confirm commits ahead of origin/main**

```bash
git log --oneline origin/main..HEAD
```
Expected: list of commits from Tasks 0–9 (Task 10 + 11 are verification-only, may add 0 or 1 fix commits).

- [ ] **Step 3: Ask Holden for explicit ship approval**

Pause. Ask Holden in chat:
> *"v0.0.4 ready to push to origin/main. New skills, retrofits, version bumps, README + CHANGELOG all committed. Ready to ship?"*

Wait for explicit approval. If declined: stop. If approved, continue.

- [ ] **Step 4: Push to origin**

```bash
cd ~/Claude/holden-alt/realty-stack
git push origin main
```
Expected: push succeeds; no force-push needed.

- [ ] **Step 5: Tag v0.0.4**

```bash
cd ~/Claude/holden-alt/realty-stack
git tag v0.0.4
git push origin v0.0.4
```
Expected: tag pushed; visible at `https://github.com/holden-alt/realty-stack/releases/tag/v0.0.4`.

- [ ] **Step 6: Verify GitHub state**

```bash
gh repo view holden-alt/realty-stack
gh release list --repo holden-alt/realty-stack | head -5
```
Expected: v0.0.4 listed; main branch matches local HEAD.

- [ ] **Step 7: Final confirmation message**

Tell Holden:
> *"v0.0.4 shipped. Plugin manifest updated; new skills live; tab + print retrofits in place. Verify in a fresh Claude Code session by running `claude plugin marketplace update realty-stack` and confirming the version shows 0.0.4."*

---

## Self-review

Plan written and self-checked:

### 1. Spec coverage

| Spec section | Task(s) |
|---|---|
| `/listing-presentation-template` Steps A–H | Task 4 |
| Template file format | Task 4 |
| `/listing-presentation` Steps 1–5 | Task 5 |
| Sub-project D — Tab visibility retrofit (Retrofit 1) | Task 0 (canonical), Task 1 (new template), Task 2 (seller), Task 3 (buyer) |
| Sub-project D — Print CSS retrofit (Retrofit 2) | Task 0 (canonical), Task 1 (new template), Task 2 (seller), Task 3 (buyer) |
| `output-style-guide.md` §10 + §11 | Task 0 |
| Architecture (file layout) | File Structure (top of plan) |
| Sibling-skill consumption (voice + brand + optional /cma) | Tasks 4, 5 (in SKILL.md bodies) |
| Optional inline /cma offer at Step 3 of /listing-presentation | Task 5 (Step 3) |
| `using-realty-stack` overlay catalog update | Task 7 |
| Slash command wrappers | Task 6 |
| Edge case tables | Tasks 4, 5 (SKILL.md bodies) |
| "What these skills never do" | Tasks 4, 5 (SKILL.md bodies) |
| Version + plugin.json + funnel hook bumps | Task 8 |
| README + CHANGELOG | Task 9 |
| Plugin validate + smoke test | Task 10 |
| Human-in-loop e2e | Task 11 |
| GitHub push (gated) | Task 12 |

No spec section uncovered.

### 2. Placeholder scan

No "TBD" / "TODO" / "fill in later" / "handle appropriately" / vague references. All steps contain:
- Exact file paths
- Concrete code blocks (CSS, HTML, JSON, bash, markdown)
- Exact commands with expected output
- Exact commit messages via HEREDOC + Co-Authored-By trailer

### 3. Type / path consistency

Cross-task identifier check:

- `~/.config/realty-stack/listing-presentation-template.md` — consistent across Tasks 4, 5, 11
- `skills/listing-presentation-template/SKILL.md` — consistent across Tasks 4, 6, 10
- `skills/listing-presentation/SKILL.md` — consistent across Tasks 5, 6, 10
- `skills/listing-presentation/references/html-template-listing-presentation.html` — consistent across Tasks 1, 5, 11
- `skills/cma/references/output-style-guide.md` — consistent across Tasks 0, 1, 2, 3
- `skills/cma/references/html-template-seller.html` — consistent across Tasks 2, 11 (regression check)
- `skills/cma/references/html-template-buyer.html` — consistent across Tasks 3, 11
- Slash command names: `/listing-presentation-template` and `/listing-presentation` — no drift to `/listing-pres-template` or similar
- Tab IDs: `who`, `how`, `track`, `working` — consistent in Task 1 (HTML template), Task 5 (SKILL.md SECTION_LIST_TAB_N references)
- Placeholder names (`{{SELLER_NAME}}`, `{{PROPERTY_ADDRESS}}`, `{{APPOINTMENT_DATE}}`, `{{CUSTOM_NOTE}}`, `{{SECTION_LIST_TAB_N}}`, etc.) — consistent between Task 1 (template) and Task 5 (skill that substitutes)
- Funnel hook footer literal `✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon` — consistent across Tasks 1, 4, 5, 8

### 4. Task ordering

Logical:
- Task 0 (canonical patterns) BEFORE Tasks 1, 2, 3 (templates that apply them) — patterns documented before they're used
- Task 1 (new template) BEFORE Tasks 2, 3 (retrofits) — new template is the visual reference; retrofits back-apply the same pattern
- Tasks 2, 3 (HTML retrofits) BEFORE Tasks 4, 5 (skill SKILL.md bodies) — output templates exist before skills reference them
- Task 4 BEFORE Task 5 — `/listing-presentation-template` is the prerequisite for `/listing-presentation` (Task 5 SKILL.md references it for the inline fallback)
- Tasks 4, 5 BEFORE Task 6 — slash command wrappers reference the skills
- Task 7 (overlay catalog) BEFORE Task 8 (version bump + footers) — version bump touches the overlay file's footer
- Task 8 BEFORE Task 9 — README + CHANGELOG reference the new version
- Task 10 (smoke test) AFTER all functional + manifest changes
- Task 11 (e2e) AFTER Task 10 — smoke test confirms routing before Holden invests in the full e2e
- Task 12 (push) LAST and gated

### 5. Commit hygiene

Each task ends in one commit. Commit messages via HEREDOC for formatting. Co-Authored-By trailer on every commit. Stages only files relevant to that task (no `git add -A`).

### 6. Funnel hook + voice / brand contracts

- v0.0.4 footer text reused exactly across all skill files
- Voice profile contract from CLAUDE.md respected (Email Voice for long-form prose; agent profile fields pulled, never asked)
- Brand kit contract respected (assets base64-embedded, accent is pigment-only, wordmark CSS-rendered)
- Fair housing compliance flagged in Step E of Task 4 (testimonials with protected-class language) and Step E generally (no fair housing red flags in any section)
- "Show before do" T18 respected — no auto-save in /listing-presentation-template; per-listing /listing-presentation writes only after Step 1 personalization is collected
- "No personification" T16 respected — funnel hook footer is on the output but the body never says "Realty Stack" or "Realty Brain" in the realtor-facing prose

### 7. Open questions surfaced from the spec

The spec's 10 open questions are decisions still open at implementation time:

1. **Tab affordance exact CSS:** ✅ resolved in Task 0 — canonical block specified, applied verbatim across Tasks 1, 2, 3
2. **Print CSS exact rules:** ✅ resolved in Task 0 — canonical block specified, applied verbatim
3. **Update vs fresh template mode (Step A):** Task 4 spec section explicitly lists three paths
4. **Custom section tab assignment:** Task 4 spec section requires the section-to-tab classification flow
5. **Past-listing render count default:** Task 4 spec covers (top 6 by recency, agent override)
6. **Agent photo source priority:** Task 4 + Task 1 — `headshot_override` field in template; brand kit headshot is default
7. **Section assignment-to-tab encoding:** Task 4 — template format `[Tab: <name>]` syntax + validation
8. **Mobile fallback for new tab affordance:** Task 0 §10 covers (retain native `<select>` below 600px)
9. **`/cma` inline offer copy:** Task 5 (Step 3 verbatim copy)
10. **HTML parameterization style:** Task 1 — same `{{PLACEHOLDER}}` pattern as `/cma`

All resolved or explicitly scoped in tasks. No spec-level question deferred to implementation guess.

Plan complete. Ready for execution.
