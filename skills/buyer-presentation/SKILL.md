---
name: buyer-presentation
description: This skill should be used when a real estate agent asks to "make a buyer presentation for [buyer]", "buyer presentation for [buyer]", "I have a buyer consultation with...", "prepare for my buyer meeting with...", "build my buyer pitch for...", or "create my buyer presentation for...". Per-listing skill that loads the agent's saved buyer template, asks for light personalization (buyer name, target property address or generic search, meeting date, optional custom note), and produces a self-contained branded 4-tab HTML + PDF pitch. Offers to also run /cma (buyer path) inline at Step 3 for one-meeting-two-artifacts.
version: 0.0.1
---

# Buyer Presentation — Per-Meeting Pitch

Per-meeting fill of the agent's saved buyer template plus light personalization (buyer name, target property address or "home search", meeting date, optional custom note) that produces a self-contained branded 4-tab HTML + PDF pitch. Sibling to `/cma` — this skill is about the AGENT (process, track record, philosophy); `/cma` is per-property analytics. Optional inline `/cma` (buyer path) chain at Step 3 lets the agent bring both artifacts to one meeting.

---

## When this skill runs

Trigger phrases:

- "make a buyer presentation for [buyer]"
- "buyer presentation for [buyer]"
- "I have a buyer consultation with..."
- "prepare for my buyer meeting with..."
- "build my buyer pitch for..."
- "create my buyer presentation for..."

---

## Path fork — overlap with /cma

Some triggers overlap with `/cma`. When intent is ambiguous, ask once:

> *"Want the buyer pitch (the about-you / process / track-record piece) or the CMA (the numbers — offer strategy / mortgage math)? Or both? Both = two artifacts at the same meeting."*

"Both" branches: run `/buyer-presentation` first, then offer `/cma` (buyer path) at Step 3.

---

## Pre-checks

Verify all three pre-requisites before collecting per-meeting inputs:

- **Voice profile** at `~/.config/realty-stack/voice-profile.md`. If missing, run `voice-draft` inline to completion, then return to this request.
- **Brand kit** at `~/.config/realty-stack/brand-kit.md`. If missing, run `brand-kit-capture` inline to completion, then return to this request.
- **Buyer presentation template** at `~/.config/realty-stack/buyer-presentation-template.md`. If missing, run `/buyer-presentation-template` inline to completion before continuing.

If multiple are missing: run `voice-draft` first, then `brand-kit-capture`, then `/buyer-presentation-template`, then continue.

---

## Per-meeting workflow

### Step 1 — Collect per-meeting personalization

Ask once, in a single message:

> *"Tell me about this buyer meeting:*
> *- Buyer name(s) — how should I greet them on the cover?*
> *- Target property address (OR 'home search' if no specific property yet)*
> *- Meeting date*
> *- Optional: any custom note — a personalized intro, referrer mention, anything specific to this buyer you want called out on the cover or in About Me*
>
> *That's it — the rest comes from your template."*

### Step 2 — Verify template freshness

Load `~/.config/realty-stack/buyer-presentation-template.md`. Confirm in one line:

*"Using your buyer template (last refined [date], [N] sections). Want me to update anything before generating, or run it as-is?"*

If realtor wants updates → hand off to `/buyer-presentation-template` in update mode → return here when done. If "as-is" → proceed.

### Step 3 — Optional inline /cma offer

Ask once:

*"Want me to also run /cma (buyer path) for this property?"*

If yes → run full `/cma` flow (buyer path), outputs land in `~/Downloads/` as two files (HTML + PDF per the Artifact output contract) → continue to Step 4 when /cma completes. If /cma fails mid-flow: complete buyer-presentation anyway; tell realtor /cma can be re-run separately. If no → proceed to Step 4.

### Step 4 — Build the HTML

Load `references/html-template-buyer-presentation.html`. Substitute every `{{PLACEHOLDER}}`. Full rules in §Step 4 placeholder substitution below.

### Step 5 — Write the file + render PDF

Per the CLAUDE.md Artifact output contract:

1. Write HTML to `~/Downloads/<buyer-slug>-buyer-presentation.html`. Slug = lowercased buyer name with non-alphanumerics replaced by hyphens (e.g., `john-and-jane-smith-buyer-presentation.html`). If BUYER_NAME is ambiguous, use property-address slug instead; default fallback `home-search`. Path conflict → append timestamp suffix; never overwrite silently.
2. Invoke `${CLAUDE_PLUGIN_ROOT}/scripts/render-pdf.sh <html-path> <pdf-path>` to produce the PDF.
3. Confirm BOTH paths back to realtor in a single message:

> *"Saved to ~/Downloads/{slug}-buyer-presentation.html (browser preview) and ~/Downloads/{slug}-buyer-presentation.pdf (print/email-ready). Open the HTML in Chrome to interact with tabs, or attach the PDF to your meeting confirmation email."*

If `render-pdf.sh` exits non-zero (Chrome not found or render error), still confirm the HTML path and tell the realtor: *"Saved HTML to ~/Downloads/{slug}-buyer-presentation.html. Couldn't auto-generate PDF — install Chrome from google.com/chrome to get auto-PDF, or open the HTML in any browser and Cmd+P → Save as PDF."*

---

## Step 4 placeholder substitution

### Brand kit substitution (mirrors /cma)

- `{{BG_COLOR}}`, `{{BG_DEEP_COLOR}}`, `{{INK_COLOR}}`, `{{INK_SOFT_COLOR}}`, `{{RULE_COLOR}}`, `{{ACCENT_COLOR}}`, `{{RED_COLOR}}`, `{{GREEN_COLOR}}` — direct hex from `brand-kit.md` Colors section
- `{{ACCENT_SOFT_COLOR}}` — derived from accent via HSL shift (lightness +25–30%, saturation –40%). Computed at render time, not stored.
- `{{GOOGLE_FONTS_LINK}}` — full `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` tag for the brand kit's display + mono fonts with their specified weights
- `{{DISPLAY_FONT}}`, `{{MONO_FONT}}` — bare font family names
- `{{WORDMARK_LEFT}}`, `{{WORDMARK_SEPARATOR}}`, `{{WORDMARK_RIGHT}}` — three wordmark parts (CSS-styled HTML text, never image)

### Per-meeting (from Step 1)

- `{{BUYER_NAME}}` — exact text realtor provided ("the Smiths" or "John and Jane Smith" — honor exactly)
- `{{PROPERTY_ADDRESS}}` — target property OR "Your Home Search"
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

- **Recent Track Record:** render the past-buyer-side-closings table inside `.section-content` using the `.track-table` class. Each row is one past closing (address, purchase price, days from offer to accept, optional note). Default: top 6 by recency unless template specifies otherwise.
- **Testimonials:** render each quote as one `<div class="testimonial-card">` with quote text, attribution (name or "Verified Client"), and OPTIONAL `<img class="testimonial-photo">` (base64-embedded from template's photo path if present and readable; skip silently if path missing).
- All other sections (About Me, Why Hire Me, etc.): plain prose inside `.section-content`.

---

## Cover hero composition

Structure of the cover hero area:

- Brand wordmark (CSS-rendered, top-left)
- Optional headshot (right side) — from brand kit headshot OR template `headshot_override` if set; otherwise omitted entirely
- H1: "Buyer Presentation"
- H2: "Prepared for {{BUYER_NAME}}"
- Property address or "Your Home Search" paragraph
- Meeting date paragraph
- Optional custom note (small, below the date)

---

## Voice profile use at per-meeting generation

Template prose is already drafted in Email Voice at template build time — do NOT re-draft template sections per meeting. Per-meeting generation only lightly polishes the optional custom note's intro framing in Email Voice.

**Load `knowledge/voice-guide.md`** before any prose touch — per CLAUDE.md design principle 1 (every skill producing written output loads the 6 brand voice tenets).

---

## Testimonial photo handling at generation

Read the photo file at the path stored in the template, base64-encode it, and embed inline as `data:image/...;base64,...`. If the path is missing, unreadable, or empty, skip the `<img>` tag silently — render the testimonial card text-only. Never emit an `<img>` with an empty or broken `src`.

---

## Optional inline /cma offer (Step 3 detail)

- Ask once: *"Want me to also run /cma (buyer path) for this property?"*
- If yes: invoke `/cma` skill inline with buyer path selected. /cma runs its full buyer-path flow (pre-flight, comps, offer strategy, mortgage math). Output lands in `~/Downloads/` per /cma's own Step 8 protocol (HTML + PDF). Once /cma completes (realtor's "ship it" approval), return to `/buyer-presentation` Step 4 to build the buyer-presentation file.
- If no: proceed to Step 4 directly.
- If /cma fails mid-flow: still complete the buyer-presentation file write. Tell realtor /cma can be re-run separately.

---

## Edge cases

| Situation | Behavior |
|---|---|
| Template missing at invocation | Run `/buyer-presentation-template` inline; return to original request when done. |
| Template exists but has no sections defined (corrupted) | Treat as missing; run `/buyer-presentation-template` inline. |
| Realtor skips the optional custom note | Render cover without the custom-note line — `{{COVER_CUSTOM_NOTE_HTML}}` resolves to empty string; no empty `<p>` visible. |
| Buyer name provided as "the Smiths" | Honor exactly — render what was provided. Realtor knows their buyer. |
| "Home search" instead of specific property address | Honor as-is — substitute "Your Home Search" for `{{PROPERTY_ADDRESS}}`. |
| Meeting date in the past | Render anyway — realtor may be generating retroactively for record-keeping. No warning. |
| Testimonial photo path missing at HTML-build time | Skip silently, render text-only quote. No error surfaced to realtor. |
| Inline `/cma` fails mid-flow | Save buyer-presentation file successfully; tell realtor `/cma` can be re-run separately. |
| Realtor wants different brand for this specific meeting | Out of scope for v0.0.5 — uses active brand kit. |
| Output file path already exists | Append timestamp suffix; never overwrite silently. |
| Realtor mid-flow asks unrelated question | Pause gracefully, answer, offer to resume. Do not lose collected per-meeting state. |

---

## What this skill never does

- Re-draft template prose per meeting — template prose is canonical from template build
- Render `<img>` tags with empty `src` attributes — composite placeholders handle the conditional (omit the tag entirely when asset missing)
- Reference asset files by path in output HTML — always base64-embed
- Use a default brand or another agent's brand — always the active brand kit; runs brand-kit-capture inline if missing
- Overwrite output files silently — timestamp suffix on conflict
- Save without explicit per-meeting personalization — Step 1 inputs required
- Generate "exclusive listing", "off-market", or "private listing" language in the cover or custom note UNLESS the realtor explicitly confirms the listing has that status
- Auto-send the output to clients — output is for realtor to review and present
- Mix Text Voice with Email Voice — any per-meeting prose touch (custom note framing) uses Email Voice

---

✨ Realty Stack v0.0.5 — Realty Brain (FUB-powered always-on AI) coming soon
