# CMA Output — Visual Style Guide

Reference doc for all HTML templates produced by the `/cma` skill. This guide documents HOW to use the brand kit values — discipline, patterns, mobile behavior. The brand kit (`brand-kit-capture`) provides the raw COLORS / FONTS / WORDMARK values that get substituted in.

---

## 1. Visual Design System

### Color palette

Eight CSS custom properties are set from the brand kit at template render time. Use them by variable name only — never hardcode hex values in templates.

```css
--bg:       <brand-kit>  /* Limestone — page background */
--bg-deep:  <brand-kit>  /* Limestone deep — input panel, table headers */
--ink:      <brand-kit>  /* Near-black — primary contrast */
--ink-soft: <brand-kit>  /* Soft ink — body text */
--rule:     <brand-kit>  /* Border color */
--accent:   <brand-kit>  /* Brass — accent pigment only, see §2 */
--red:      <brand-kit>  /* Caveat / warning */
--green:    <brand-kit>  /* Positive adjustment */
```

Default values (Holden/GR brand, fallback when brand kit absent):

```css
--bg: #F4F3EF;
--bg-deep: #E8E6DF;
--ink: #111418;
--ink-soft: #3A3F46;
--rule: #C7C4BC;
--accent: #B08A44;
--red: #963c2a;
--green: #3d6b3d;
```

### Typography sizing scale

| Role | Spec |
|---|---|
| Body base | 15px / 1.55 line-height / Inter 400 |
| Body emphasis | Inter 500 |
| H2 | `clamp(28px, 4vw, 36px)` / Inter 600 / tracking -0.03em |
| H3 | 18px / Inter 600 / tracking -0.025em |
| H4 | 15px / Inter 600 |
| Mono (labels, captions, data) | 10–11px / JetBrains Mono 400–500 / `letter-spacing: 0.18em` / uppercase |

Two font families, declared as variables:

```css
--fd: 'Inter';           /* Display + body — weights 400/500/600/700 */
--fm: 'JetBrains Mono';  /* Captions, labels, numeric data — weights 400/500 */
```

Load both via a single Google Fonts request. Inter and JetBrains Mono are the only permitted typefaces.

### Geometric discipline

Apply these rules to every element unless a specific pattern below explicitly overrides:

- `border-radius: 0` — no rounded corners anywhere
- `border: 1px solid var(--rule)` — hairline only, never thicker
- No `box-shadow` — no drop shadows, no inset shadows
- No gradients — the single permitted exception is the cover top bar (brand-permitted decorative moment); nowhere else

---

## 2. Brand Discipline Rules

### Accent (brass) is a pigment, not a fill

Accent color (`--accent`) carries visual weight precisely because it is sparse. Use it in exactly these roles:

**Permitted uses — one element per role:**
- A single character (the slash in the wordmark)
- A thin bar (left border on callouts, top border on result panel)
- Single mono-caption color (section captions, labels)
- Single decorative element per panel (timeline dot, divider mark)

**Prohibited uses:**
- Background fill on any card, button, badge, or container
- Any gradient or shadow value
- Text emphasis on more than one word at a time
- Hover/focus state backgrounds

If you find yourself reaching for `background: var(--accent)`, stop. That is a fill. Redesign as a border or a single character.

### Color pairing constraints

- Ink background (`--ink`) pairs with `--bg` or `--bg-deep` text — never `--accent` text at body size
- Limestone background (`--bg`, `--bg-deep`) pairs with `--ink` or `--ink-soft` body text
- Mono labels on ink backgrounds: `--accent` (approved pigment use)
- Mono labels on limestone backgrounds: `--ink-soft`

---

## 3. Wordmark Rendering Pattern

Render the agent's wordmark as HTML/CSS text, NOT a PNG. Benefits:

- Sharp at any screen resolution and in print
- No image dependency — the HTML file is fully self-contained
- Matches brand spec exactly
- Substitutable via template variables

```html
<div class="wordmark">{{WORDMARK_LEFT}}<span class="slash">{{WORDMARK_SEPARATOR}}</span>{{WORDMARK_RIGHT}}</div>
```

```css
.wordmark {
  font-family: var(--fd);
  font-weight: 600;
  font-size: 22px;
  letter-spacing: -0.03em;
  color: var(--ink);
}
.wordmark .slash {
  color: var(--accent);
}
```

The brand kit provides three substitution tokens:
- `{{WORDMARK_LEFT}}` — text before the separator (e.g. "Holden")
- `{{WORDMARK_SEPARATOR}}` — the separator character (e.g. "/")
- `{{WORDMARK_RIGHT}}` — text after the separator (e.g. "GR")

When `{{WORDMARK_SEPARATOR}}` is a slash, `.slash { color: var(--accent) }` is the single permitted accent-as-character use. If the brand uses a different separator, apply the same class — the accent rule still holds.

---

## 4. Section Header Pattern

The brand-native panel opener. Use this structure for every major section in the CMA:

```html
<div class="panel-header">
  <div class="mono panel-caption">01 / OVERVIEW</div>
  <h2>Executive overview</h2>
  <div class="panel-subtitle">The recommendation, the evidence, the strategy</div>
</div>
```

Rules:
- Mono caption always sits **above** the H2 — never below, never to the side
- Caption follows the format `NN / LABEL` where `NN` is two-digit section number
- Caption uses `--accent` color (the permitted mono-label use)
- H2 uses `clamp(28px, 4vw, 36px)` with tracking -0.03em
- Subtitle is Inter 400 15px, `--ink-soft`

CSS:

```css
.panel-caption {
  font-family: var(--fm);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 8px;
}
.panel-header h2 {
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 600;
  letter-spacing: -0.03em;
  color: var(--ink);
  margin: 0 0 6px;
}
.panel-subtitle {
  font-size: 15px;
  color: var(--ink-soft);
}
```

---

## 5. Ink Callout Pattern

Use for strategic takeaways, key recommendations, and high-signal conclusions. The ink background creates strong visual separation from the limestone page.

```html
<div class="callout-ink">
  <div class="mono">STRATEGIC TAKEAWAY</div>
  <p>Body text in limestone... with <em>brass-emphasized word</em> for accent.</p>
</div>
```

CSS:

```css
.callout-ink {
  background: var(--ink);
  border-left: 3px solid var(--accent);
  padding: 20px 24px;
  color: var(--bg);
}
.callout-ink .mono {
  font-family: var(--fm);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 10px;
}
.callout-ink em {
  color: var(--accent);
  font-style: normal;
}
```

Accent appears in three places: left border (thin bar), mono caption, and the single `<em>`. That is the maximum. Never use `<em>` on more than one word per callout.

---

## 6. Mobile Patterns

### Critical lesson: horizontal-scroll tabs DO NOT WORK on mobile

The first three mobile iterations of the 6333 Blackmar build failed because they used horizontal-scrolling tab bars. Users do not reliably recognize horizontal scroll as a navigation affordance. Tested with the actual agent — he could not navigate between sections.

**Do not build horizontally-scrolling tab bars for mobile. They look like they work. They do not.**

### Solution: native `<select>` dropdown on mobile

Hide the desktop tab bar below 768px. Show a styled `<select>` that opens the iOS/Android native picker.

HTML (include both in every tabbed template):

```html
<!-- Desktop tab bar — hidden on mobile -->
<nav class="tabs">
  <button class="tab-btn active" data-tab="overview">Overview</button>
  <button class="tab-btn" data-tab="comps">Comparables</button>
  <button class="tab-btn" data-tab="adjustments">Adjustments</button>
  <button class="tab-btn" data-tab="valuation">Valuation</button>
  <button class="tab-btn" data-tab="netsheet">Net Sheet</button>
</nav>

<!-- Mobile nav — hidden on desktop -->
<div class="mobile-nav">
  <label class="mobile-nav-label">Section</label>
  <select id="mobileTabSelect">
    <option value="overview">01 · Overview</option>
    <option value="comps">02 · Comparables</option>
    <option value="adjustments">03 · Adjustments</option>
    <option value="valuation">04 · Valuation</option>
    <option value="netsheet">05 · Net Sheet</option>
  </select>
</div>
```

CSS:

```css
/* Desktop default */
.mobile-nav { display: none; }

@media (max-width: 768px) {
  nav.tabs { display: none; }

  .mobile-nav {
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 9;
    background: var(--ink);
    padding: 10px 16px;
    border-bottom: 1px solid var(--accent);
  }

  .mobile-nav-label {
    font-family: var(--fm);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    white-space: nowrap;
  }

  #mobileTabSelect {
    flex: 1;
    height: 44px;          /* Apple HIG minimum tap target */
    background: var(--ink);
    color: var(--bg);
    border: 1px solid var(--accent);
    border-radius: 0;
    font-family: var(--fd);
    font-size: 14px;
    padding: 0 32px 0 10px;
    appearance: none;
    -webkit-appearance: none;
    /* Custom chevron via SVG data URI */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23B08A44' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    cursor: pointer;
  }
}
```

JavaScript — wire both controls to the same function and keep them in sync:

```javascript
function switchToTab(target) {
  // Hide all panels
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

  // Show target panel
  const panel = document.getElementById(target);
  if (panel) panel.classList.add('active');

  // Sync desktop tab button
  const btn = document.querySelector(`.tab-btn[data-tab="${target}"]`);
  if (btn) btn.classList.add('active');

  // Sync mobile select
  const sel = document.getElementById('mobileTabSelect');
  if (sel) sel.value = target;
}

// Desktop tab buttons
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => switchToTab(btn.dataset.tab));
});

// Mobile select
document.getElementById('mobileTabSelect').addEventListener('change', e => {
  switchToTab(e.target.value);
});
```

### Comp summary on mobile

On desktop, comp rows are a single-row flex/grid with: `[ID] [Address+meta] [Sold price] [Adj value] [Chevron]`. On a 375px screen, sold price and adjusted value both get cut off.

Restructure as a 2-row grid — no HTML changes needed, CSS grid placement only:

```
Row 1:  [ID]  [Address + meta]              [Chevron]
Row 2:  [Sold: $459,900]      [Adj: $531,357]
```

```css
@media (max-width: 768px) {
  .comp-summary {
    display: grid;
    grid-template-columns: 32px 1fr 22px;
    grid-template-rows: auto auto;
    gap: 4px 8px;
    padding: 12px 14px;
  }

  /* Row 1 */
  .comp-summary > *:nth-child(1) { grid-column: 1; grid-row: 1; }      /* ID badge */
  .comp-summary > *:nth-child(2) { grid-column: 2; grid-row: 1; }      /* Address + meta */
  .comp-summary > *:nth-child(5) { grid-column: 3; grid-row: 1; }      /* Chevron */

  /* Row 2 */
  .comp-summary > *:nth-child(3) { grid-column: 1 / 3; grid-row: 2; } /* Sold price */
  .comp-summary > *:nth-child(4) { grid-column: 3 / 4; grid-row: 2; } /* Adj value */
}
```

Both prices remain visible. No layout rewrite needed in the HTML.

### Tables on mobile

Wrap every wide table in a scroll container. Never let a table overflow the viewport without containment.

```html
<div class="table-scroll">
  <table>...</table>
</div>
```

```css
.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.table-scroll table {
  min-width: 540px;  /* adjust per table — enough for all columns to be readable */
}
```

### Calculator inputs on mobile

When a text input has a prefix element (`$`, `%`), do not set `width: 100%` on the input — it will overflow past the prefix. Use:

```css
@media (max-width: 768px) {
  .calc-input {
    width: calc(100% - 28px);  /* 28px = prefix element width */
  }
}
```

### Tap targets

All interactive elements must meet 44px minimum height per Apple HIG. Apply to:

- All `<button>` elements
- The mobile `<select>`
- Desktop tab buttons (`.tab-btn`)
- Preset chips

```css
button, .tab-btn, .preset-chip, select {
  min-height: 44px;
}
```

### Smallest phones (iPhone SE, ≤380px)

Add a secondary breakpoint for the tightest layouts:

```css
@media (max-width: 380px) {
  /* Subject card grid: collapse to single column */
  .subject-grid {
    grid-template-columns: 1fr;
  }

  /* Hero stat values: reduce font size */
  .hero-stat-value {
    font-size: clamp(22px, 6vw, 28px);
  }

  /* Calculator input: tighten further */
  .calc-input {
    width: calc(100% - 24px);
  }

  /* Preset chips: tighter padding */
  .preset-chip {
    padding: 8px 10px;
    font-size: 12px;
  }
}
```

### Viewport meta

Every template must include:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

- `viewport-fit=cover` — handles iPhone notch / Dynamic Island correctly
- Do NOT add `maximum-scale=1` or `user-scalable=no` — those harm accessibility (pinch-to-zoom for users who need it)

---

## 7. Print Compatibility

Every tabbed template must include a `@media print` block that:

1. Makes all tab panels visible (not just the active one)
2. Forces page breaks between major sections
3. Expands all `<details>` accordions
4. Hides interactive controls that have no meaning on paper
5. Strips body texture and pseudo-element overlays

```css
@media print {
  /* Show every panel regardless of active state */
  .tab-panel {
    display: block !important;
    page-break-after: always;
  }

  /* Expand all accordions */
  details,
  details > * {
    display: block !important;
  }
  details[open] summary::after,
  details summary::marker {
    display: none;
  }

  /* Hide interactive-only elements */
  nav.tabs,
  .mobile-nav,
  .preset-chips,
  .reset-btn,
  .tab-btn {
    display: none !important;
  }

  /* Strip texture overlays */
  body::before,
  body::after {
    display: none !important;
  }

  /* Ensure ink-on-white legibility */
  body {
    background: #fff;
    color: #000;
  }

  /* Prevent orphaned section headers */
  .panel-header {
    page-break-after: avoid;
  }

  /* Keep comp rows together */
  .comp-row {
    page-break-inside: avoid;
  }
}
```

Print output should be agent-shareable as a PDF without requiring any browser extension or special configuration.

---

## Quick Reference Checklist

Before shipping any CMA HTML template, verify:

- [ ] All color references use CSS custom properties (`var(--x)`), never hardcoded hex
- [ ] `border-radius: 0` on all elements — no rounded corners
- [ ] `--accent` appears only as: slash character, thin border, mono label, or single decorative mark
- [ ] Wordmark rendered as HTML/CSS text with `{{WORDMARK_*}}` tokens, not an image
- [ ] Section headers follow `mono caption → H2 → subtitle` order
- [ ] Mobile: `nav.tabs` hidden at ≤768px, `.mobile-nav` select visible
- [ ] Both tab controls wired to same `switchToTab()` function
- [ ] Comp summary uses 2-row grid placement at ≤768px
- [ ] All tap targets ≥44px height
- [ ] Viewport meta includes `viewport-fit=cover`, omits `maximum-scale`
- [ ] `@media print` block shows all panels, hides interactive controls
