---
name: cma
description: Create a CMA presentation — comparative market analysis with branded HTML output. Seller mode (4-tab listing presentation) or buyer mode (3-tab offer strategy). Forks on first clarifying question. Live nationwide research per invocation.
---

Run the /cma workflow. This skill produces a self-contained branded HTML CMA presentation.

If the user provided context (address, "for [client]", buyer/seller hint) in their slash invocation, use it to skip clarifying questions where possible. Otherwise start with the standard CMA pre-flight: clarify buyer or seller, then aggressive or conservative, then collect subject + comps + condition ratings.

Full workflow documented at `${CLAUDE_PLUGIN_ROOT}/skills/cma/SKILL.md` — follow it exactly.
