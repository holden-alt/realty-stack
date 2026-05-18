---
name: buyer-presentation-template
description: Build the agent's reusable buyer-presentation template (one-time consultative onboarding). State scan offers to inherit shared sections (About Me, Why Hire Me, Track Record, Testimonials) from listing-presentation-template if present. Hybrid front-loaded data dump → categorize into 8 standard buyer-side sections → draft Email Voice → refine → save to ~/.config/realty-stack/buyer-presentation-template.md.
---

Run the /buyer-presentation-template workflow. One-time consultative builder that captures the agent's reusable buyer-side pitch content (about-me, why-hire-me, buying-process, how-i-find-homes, track-record, testimonials, negotiation-philosophy, buyer-rep-agreement).

If a listing-presentation-template already exists, Step 0 offers to inherit 4 shared sections — realtor only fills the 4 buyer-specific ones. If the user already has a buyer-presentation-template at `~/.config/realty-stack/buyer-presentation-template.md`, ask whether to update specific sections, start fresh, or cancel.

Full workflow documented at `${CLAUDE_PLUGIN_ROOT}/skills/buyer-presentation-template/SKILL.md` — follow it exactly.
