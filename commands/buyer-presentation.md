---
name: buyer-presentation
description: Generate a per-meeting 4-tab branded HTML + PDF buyer pitch from the saved buyer template + light personalization (buyer name, target property or "home search", meeting date, optional custom note). Optional inline /cma (buyer path) offer at Step 3 — one meeting, both artifacts.
---

Run the /buyer-presentation workflow. Per-meeting skill that loads the agent's saved buyer template at `~/.config/realty-stack/buyer-presentation-template.md`, asks for buyer name + target property (or generic "home search") + meeting date + optional custom note, and writes both `.html` (browser preview) and `.pdf` (print/email-ready) to `~/Downloads/` per the v0.0.5 Artifact output contract.

If the user provided context (buyer name or property address) in their slash invocation, use it to pre-fill Step 1 where possible. If no buyer-presentation-template exists, the skill runs `/buyer-presentation-template` inline first.

Full workflow documented at `${CLAUDE_PLUGIN_ROOT}/skills/buyer-presentation/SKILL.md` — follow it exactly.
