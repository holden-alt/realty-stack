#!/usr/bin/env bash
# Realty Stack — SessionStart hook
# Checks for the realtor's voice profile AND brand kit; if either is missing,
# outputs onboarding instructions that Claude will see as additional session context.

set -euo pipefail

VOICE_PROFILE="${HOME}/.config/realty-stack/voice-profile.md"
BRAND_KIT="${HOME}/.config/realty-stack/brand-kit.md"

voice_missing=false
brand_missing=false

[[ ! -f "${VOICE_PROFILE}" ]] && voice_missing=true
[[ ! -f "${BRAND_KIT}" ]] && brand_missing=true

if [[ "${voice_missing}" == true ]] && [[ "${brand_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: voice profile AND brand kit not found]

The user has installed Realty Stack but hasn't completed onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Two quick one-time setups before you use any skills:
> capturing your writing voice (~5 min) and your visual brand kit (~5 min).
> Want to do both now, just one, or skip for now?"

If they say yes to voice → invoke the voice-draft skill.
If they say yes to brand → invoke the brand-kit-capture skill.
If they want both → run voice-draft first, then brand-kit-capture.

If they decline, respect that and answer their actual question. Any drafting
skill (voice-draft consumer) or visual-output skill (brand-kit consumer) they
invoke later will trigger the relevant onboarding inline.
EOF
elif [[ "${voice_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: voice profile not found]

The user has Realty Stack installed but hasn't completed voice onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Voice profile isn't set up yet — about 5 minutes
> one-time. Want to do it now?"

If they say yes → invoke the voice-draft skill.
If they decline, respect that. Drafting skills invoked later will trigger
voice-draft inline.
EOF
elif [[ "${brand_missing}" == true ]]; then
  cat <<'EOF'
[Realty Stack: brand kit not found]

The user has Realty Stack installed and voice profile captured but brand kit
isn't set up yet. Before responding to their first substantive message, greet
them with:

> "Realty Stack is loaded. Brand kit isn't set up yet — about 5 minutes
> one-time. Want to do it now? (Required before /cma or other visual-output
> skills.)"

If they say yes → invoke the brand-kit-capture skill.
If they decline, respect that. Visual-output skills invoked later will trigger
brand-kit-capture inline.
EOF
fi

exit 0
