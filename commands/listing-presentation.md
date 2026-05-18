---
name: listing-presentation
description: Generate a per-appointment 4-tab branded HTML listing presentation from the saved template + light personalization (seller, address, appointment date, optional custom note). Optional inline /cma offer at Step 3 — one appointment, both artifacts.
---

Run the /listing-presentation workflow. This skill loads the agent's saved template at `~/.config/realty-stack/listing-presentation-template.md`, asks for seller name + property address + appointment date + optional custom note, and writes a self-contained branded 4-tab HTML pitch to `~/Downloads/`.

If the user provided context (address, "for [seller]") in their slash invocation, use it to pre-fill Step 1 where possible. If no template exists, the skill runs `/listing-presentation-template` inline first.

Full workflow documented at `${CLAUDE_PLUGIN_ROOT}/skills/listing-presentation/SKILL.md` — follow it exactly.
