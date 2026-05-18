---
name: listing-presentation
description: This skill should be used when a real estate agent asks to "make a listing presentation for [address]", "listing presentation for [seller]", "I have a listing appointment with [address]", "prepare for my listing appointment", "build my pitch for [address]", or "create my listing presentation for [seller]". Per-listing skill that loads the agent's saved template, asks for light personalization (seller name, property address, appointment date, optional custom note), and produces a self-contained branded 4-tab HTML pitch. Offers to also run /cma inline at Step 3 for one-appointment-two-artifacts.
version: 0.0.1
---

# Listing Presentation — Per-Appointment Pitch

Per-listing filler that loads the agent's saved template plus light personalization (seller name, property address, appointment date, optional custom note) and produces a self-contained branded 4-tab HTML pitch. Sibling to `/cma` — this skill is about the AGENT (process, track record, philosophy); `/cma` is per-property analytics. The optional inline `/cma` chain at Step 3 lets the agent bring both artifacts to one appointment.

---

## When this skill runs

Trigger phrases:

- "make a listing presentation for [address]"
- "listing presentation for [seller]"
- "I have a listing appointment with [address]"
- "prepare for my listing appointment"
- "build my pitch for [address]"
- "create my listing presentation for [seller]"

---

## Path fork — overlap with /cma

Some triggers overlap with `/cma`. When intent is ambiguous, ask once:

> *"Want the listing pitch (the about-you / process / track-record piece) or the CMA (the numbers — what to price at)? Or both? Both = two artifacts at the same appointment."*

"Both" branches: run `/listing-presentation` first, then offer `/cma` at Step 3.

---

## Pre-checks

Verify all three pre-requisites before collecting per-listing inputs:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion, then return to this request.
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion, then return to this request.
- **Listing presentation template** at `~/.config/realty-stack/listing-presentation-template.md`. If missing, run `/listing-presentation-template` inline to completion before continuing (same fallback pattern as `/cma` → `brand-kit-capture`).

If multiple are missing: run `voice-draft` first, then `brand-kit-capture`, then `/listing-presentation-template`, then continue.

---

## Per-listing workflow

### Step 1 — Collect per-listing personalization

Ask once, in a single message:

> *"Tell me about this listing:*
> *- Seller name(s) — how should I greet them on the cover?*
> *- Property address*
> *- Appointment date*
> *- Optional: any custom note you want to add — a personalized intro, a referrer mention, anything specific to this seller you want called out on the cover or in About Me*
>
> *That's it — the rest comes from your template."*

### Step 2 — Verify template freshness

Load `~/.config/realty-stack/listing-presentation-template.md`. Confirm in one line:

*"Using your template (last refined [date], [N] sections). Want me to update anything before generating, or run it as-is?"*

If realtor wants updates → hand off to `/listing-presentation-template` in update mode → return here when done. If "as-is" → proceed.

### Step 3 — Optional inline /cma offer

Ask once:

*"Want me to also run /cma for this property?"*

If yes → run full `/cma` flow (seller path), outputs land in `~/Downloads/` as two files → continue to Step 4 when /cma completes. If no → proceed to Step 4.

### Step 4 — Build the HTML

Load `references/html-template-listing-presentation.html`. Substitute every `{{PLACEHOLDER}}`. Full rules in §Step 4 placeholder substitution below.

### Step 5 — Write the file

Default path: `~/Downloads/<property-slug>-listing-presentation.html`. Slug = lowercased street address with non-alphanumerics replaced by hyphens (e.g., `1247-plainfield-ave-ne-listing-presentation.html`). Path conflict → append timestamp suffix (`<slug>-listing-presentation-2026-05-17-1430.html`); never overwrite silently. Realtor override "save to [path]" honored.

After writing the HTML, run headless Chrome to produce a PDF:

```
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render-pdf.sh \
  ~/Downloads/{slug}-listing-presentation.html \
  ~/Downloads/{slug}-listing-presentation.pdf
```

Confirm BOTH paths back: *"Saved to ~/Downloads/{slug}-listing-presentation.html (browser preview) and ~/Downloads/{slug}-listing-presentation.pdf (print/email-ready). Open the HTML in Chrome to interact with tabs, or attach the PDF to your appointment confirmation email."*

If `render-pdf.sh` exits non-zero (Chrome not found or render error), still confirm the HTML path and tell the realtor: *"Saved HTML to ~/Downloads/{slug}-listing-presentation.html. Couldn't auto-generate PDF — install Chrome from google.com/chrome to get auto-PDF, or open the HTML in any browser and Cmd+P → Save as PDF."*

---

## Step 4 placeholder substitution

### Brand kit substitution (mirrors /cma)

- `{{BG_COLOR}}`, `{{BG_DEEP_COLOR}}`, `{{INK_COLOR}}`, `{{INK_SOFT_COLOR}}`, `{{RULE_COLOR}}`, `{{ACCENT_COLOR}}`, `{{RED_COLOR}}`, `{{GREEN_COLOR}}` — direct hex from `brand-kit.md` Colors section
- `{{ACCENT_SOFT_COLOR}}` — derived from accent via HSL shift (lightness +25–30%, saturation –40%). Computed at render time, not stored.
- `{{GOOGLE_FONTS_LINK}}` — full `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` tag for the brand kit's display + mono fonts with their specified weights
- `{{DISPLAY_FONT}}`, `{{MONO_FONT}}` — bare font family names
- `{{WORDMARK_LEFT}}`, `{{WORDMARK_SEPARATOR}}`, `{{WORDMARK_RIGHT}}` — three wordmark parts (CSS-styled HTML text, never image)

### Per-listing (from Step 1)

- `{{SELLER_NAME}}` — exact text realtor provided ("the Smiths" or "John and Jane Smith" — honor exactly)
- `{{PROPERTY_ADDRESS}}` — full street address
- `{{APPOINTMENT_DATE}}` — formatted as "Tuesday, May 20, 2026"

### Agent profile (from voice profile)

- `{{AGENT_NAME}}`, `{{AGENT_BROKERAGE}}`, `{{AGENT_PRIMARY_MARKET}}` — pulled from voice-profile.md Agent Profile section; never asked again

### Composite HTML chunks

Composite placeholders are built by the skill and substituted as full HTML or empty string — avoids broken empty tags in rendered output.

- `{{COVER_HEADSHOT_HTML}}` — if brand kit has a headshot asset (or template `headshot_override` is set), emit `<img class="agent-photo" src="data:image/...;base64,{base64}" alt="{{AGENT_NAME}}">`. If no headshot available, emit empty string.
- `{{COVER_CUSTOM_NOTE_HTML}}` — if realtor provided a custom note in Step 1, emit `<p class="custom-note">{custom_note}</p>`. If absent, emit empty string.
- `{{FOOTER_LOGO_HTML}}` — if brand kit has a logo asset, emit `<img class="footer-logo" src="data:image/...;base64,{base64}" alt="{{AGENT_BROKERAGE}}">`. If no logo, emit empty string.

### Section content (built from template)

- `{{SECTION_LIST_TAB_1}}` (Who I Am) — for each template section assigned to Tab 1, emit one `<section class="section-block">...</section>` block (see §Section rendering)
- `{{SECTION_LIST_TAB_2}}` (How I Work) — same shape for Tab 2 sections
- `{{SECTION_LIST_TAB_3}}` (Track Record) — same shape for Tab 3 sections
- `{{SECTION_LIST_TAB_4}}` (Working Together) — same shape for Tab 4 sections

---

## Section rendering — how SECTION_LIST_TAB_N is built

For each tab, iterate the template's sections assigned to that tab and emit one block per section:

```html
<section class="section-block">
  <h3>{section_title}</h3>
  <div class="section-content">
    {section_prose}
  </div>
</section>
```

**Special structured content by section type:**

- **Recent Track Record:** render the past-listings table inside `.section-content` using the `.track-table` class. Each row is one past listing (address, sale price, DOM, optional note). Default: top 6 by recency unless template specifies otherwise.
- **Testimonials:** render each quote as one `<div class="testimonial-card">` with quote text, attribution (name or "Verified Client"), and OPTIONAL `<img class="testimonial-photo">` (base64-embedded from template's photo path if present and readable; skip silently if path missing).
- All other sections (About Me, Why Hire Me, etc.): plain prose inside `.section-content`.

---

## Cover hero composition

Structure of the cover hero area:

- Brand wordmark (CSS-rendered, top-left)
- Optional headshot (right side) — from brand kit headshot OR template `headshot_override` if set; otherwise omitted entirely
- H1: "Listing Presentation"
- H2: "Prepared for {{SELLER_NAME}}"
- Property address paragraph
- Appointment date paragraph
- Optional custom note (small, below the date)

---

## Voice profile use at per-listing generation

Template prose is already drafted in Email Voice at template build time — do NOT re-draft template sections per listing. Per-listing generation only lightly polishes the optional custom note's intro framing in Email Voice (e.g., if the agent's custom note says "Thanks for the referral from Sarah Johnson", lightly polish the wording to match voice).

**Load `knowledge/voice-guide.md`** before any prose touch — per CLAUDE.md design principle 1 (every skill producing written output loads the 6 brand voice tenets).

---

## Optional inline /cma offer (Step 3 detail)

- Ask once: *"Want me to also run /cma for this property?"*
- If yes: invoke `/cma` skill inline. /cma runs its full seller-path flow (pre-flight, comps, research, draft, feedback loop). Output lands in `~/Downloads/` per /cma's own Step 8 protocol. Once /cma completes (realtor's "ship it" approval), return to `/listing-presentation` Step 4 to build the listing-presentation file.
- If no: proceed to Step 4 directly.
- If /cma fails mid-flow: still complete the listing-presentation file write. Tell realtor /cma can be re-run separately.

---

## Edge cases

| Situation | Behavior |
|---|---|
| Template missing at invocation | Run `/listing-presentation-template` inline; return to original request when done. |
| Template exists but has no sections defined (corrupted) | Treat as missing; run `/listing-presentation-template` inline. |
| Realtor skips the optional custom note | Render cover without the custom-note line — `{{COVER_CUSTOM_NOTE_HTML}}` resolves to empty string; no empty `<p>` visible. |
| Realtor provides seller name as "the Smiths" instead of "John and Jane Smith" | Honor exactly — render what was provided. Realtor knows their seller. |
| Property address ambiguous | Ask once for full street address + city; don't guess. |
| Appointment date in the past | Render anyway — realtor may be generating retroactively for record-keeping. No warning. |
| Testimonial photo path missing at HTML-build time | Skip silently, render text-only quote. No error surfaced to realtor. |
| Inline `/cma` fails mid-flow | Save listing-presentation file successfully; tell realtor `/cma` can be re-run separately. |
| Realtor wants different brand for this specific listing | Out of scope for v0.0.4 — uses active brand kit. |
| Output file path already exists | Append timestamp suffix; never overwrite silently. |
| Realtor mid-flow asks unrelated question | Pause gracefully, answer, offer to resume. Do not lose collected per-listing state. |
| Chrome / Chromium not installed | `render-pdf.sh` exits with error; skill catches it, writes HTML anyway, tells realtor: *"Saved HTML to ~/Downloads/{slug}-listing-presentation.html. Couldn't auto-generate PDF — install Chrome from google.com/chrome to get auto-PDF, or open the HTML in any browser and Cmd+P → Save as PDF."* |
| PDF rendering fails for other reason | Same fallback as above — HTML always lands; PDF is best-effort. |

---

## What this skill never does

- Re-draft template prose per listing — template prose is canonical from template build
- Render `<img>` tags with empty `src` attributes — composite placeholders handle the conditional (omit the tag entirely when asset missing)
- Reference asset files by path in output HTML — always base64-embed
- Use a default brand or another agent's brand — always the active brand kit; runs brand-kit-capture inline if missing
- Overwrite output files silently — timestamp suffix on conflict
- Save without explicit per-listing personalization — Step 1 inputs required
- Generate "exclusive listing", "off-market", or "private listing" language in the cover or custom note UNLESS the realtor explicitly confirms the listing has that status (per CLAUDE.md Do-Not list)
- Auto-send the output to clients — output is for realtor to review and present
- Mix Text Voice with Email Voice — any per-listing prose touch (custom note framing) uses Email Voice

---

✨ Realty Stack v0.0.4 — Realty Brain (FUB-powered always-on AI) coming soon
