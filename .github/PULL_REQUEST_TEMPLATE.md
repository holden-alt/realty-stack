<!-- Thanks for contributing to Realty Stack! Please fill out every section.
     PRs missing required sections will be asked to update before review. -->

## What problem did you experience?

<!-- A specific scenario from your own work, not "this could be better". 
     Example: "My follow-up draft to a hot buyer lead sounded too AI-generic. 
     I wanted X tone but got Y." -->


## What did you test?

- **Input:** <!-- the sanitized prompt or material you passed in -->
- **Output:** <!-- the relevant bit of what the skill produced -->
- **Quality:** <!-- one sentence — "felt like my voice" / "felt off because X" / etc. -->


## Did a working realtor review this diff?

<!-- Yes or No. If No, please find one before requesting review. 
     AI-assisted is fine (we build this entire bundle with AI). But every PR 
     needs a working realtor's eyes on the final diff — "no agent talks like 
     that" is the failure mode AI can't self-detect. -->


## Contracts followed (if applicable)

- [ ] **Artifact output contract** — if this is a visual-output skill, it produces BOTH `.html` and `.pdf` via `scripts/render-pdf.sh`. (See CLAUDE.md "Artifact output contract".)
- [ ] **State scan contract** — if this is an intake/onboarding skill, it has a Step 0 that scans `~/.config/realty-stack/` for inheritable content before asking the realtor for material. (See CLAUDE.md "State scan contract".)
- [ ] **Voice profile contract** — if this skill produces written output, it loads `knowledge/voice-guide.md` and matches the realtor's captured voice profile.
- [ ] **Brand kit contract** — if this skill produces visual output, it uses the captured brand kit values (colors, fonts, wordmark, base64-embedded assets).
- [ ] N/A — this PR doesn't touch contracts (bug fix, docs, etc.)


## Type of change

- [ ] New skill
- [ ] Bug fix
- [ ] Compliance language update (fair housing, NAR ethics, state disclosure)
- [ ] Docs / contract update
- [ ] Multi-harness adapter (Codex, Cursor, Gemini)
- [ ] Other: ___


## Related issue

<!-- Link the issue you opened first (per CONTRIBUTING.md step 1). 
     "Closes #123" / "Refs #123" / etc. -->


## Fair housing check (for contact-facing skills)

<!-- If this skill produces text that goes to a contact (email, text, listing 
     description, marketing copy), confirm: -->

- [ ] Fair housing pass — no protected-class targeting language, no neighborhood demographics, no "guaranteed sale" language
- [ ] N/A — this skill doesn't produce contact-facing copy
