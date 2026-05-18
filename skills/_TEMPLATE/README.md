# Skill Template

This directory is a starter scaffold for new Realty Stack skills.

## How to use

1. **Read first:**
   - [CLAUDE.md](../../CLAUDE.md) — the four canonical contracts and skill-writing conventions
   - [CONTRIBUTING.md](../../CONTRIBUTING.md) — the contribution workflow
   - One existing skill that's closest to what you're building (most likely listing-presentation-template if you're building an intake skill, or cma if you're building a visual-output skill)

2. **Copy this directory:**
   ```bash
   cp -r skills/_TEMPLATE skills/your-skill-name
   ```

3. **Edit `SKILL.md`:**
   - Replace every `<TODO>` placeholder with your skill's actual content
   - Replace `your-skill-name-here` in the frontmatter with your skill name (kebab-case)
   - Delete sections marked "DELETE THIS SECTION if..." that don't apply to your skill type
   - Follow the inline pattern references to existing skills as your guide

4. **Test on your real work** before opening a PR. Per CONTRIBUTING.md, every PR needs a real-scenario test case with sanitized input + output + quality note.

5. **Open the PR.** The PR template will walk you through what's required.

## Skill types (which sections apply)

| Skill type | Pre-checks | Step 0 scan | Artifact output |
|---|---|---|---|
| Intake / onboarding (template builder) | Yes | **Yes** | No |
| Per-invocation drafting (email, text) | Yes | No | No |
| Per-invocation visual-output (presentation, flyer) | Yes | No | **Yes** |
| Pure analysis (no realtor input, no visual output) | Maybe | No | No |

If your skill spans types, include all applicable sections.
