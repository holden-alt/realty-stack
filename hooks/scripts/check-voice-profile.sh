#!/usr/bin/env bash
# Realty Stack — SessionStart hook
# Checks for the realtor's voice profile; if missing, outputs an
# onboarding prompt that Claude will see as additional session context.

set -euo pipefail

PROFILE_PATH="${HOME}/.config/realty-stack/voice-profile.md"

if [[ ! -f "${PROFILE_PATH}" ]]; then
  cat <<'EOF'
[Realty Stack: voice profile not found]

The user has installed Realty Stack but hasn't completed voice onboarding.
Before responding to their first substantive message, greet them with:

> "Realty Stack is loaded. Before you use any skills, let's capture your
> writing voice — takes about 5 minutes, one-time. Want to do it now?"

If they say yes (or any natural affirmation), invoke the voice-draft skill
to walk them through onboarding.

If they decline or say "later," respect that and answer their actual
question — but mention that any Realty Stack drafting skill they invoke
later will trigger voice-draft inline before completing their request.
EOF
fi

exit 0
