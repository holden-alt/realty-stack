#!/usr/bin/env bash
# Render a Realty Stack listing-presentation HTML to PDF via headless Chrome.
# Usage: render-pdf.sh <input.html> <output.pdf>
#
# Why headless Chrome:
# - Realtors don't know what Cmd+P does
# - Chrome's --print-to-pdf applies @media print rules correctly
# - The canonical §7 + listing-presentation-specific print overrides
#   produce a clean 8-page PDF when rendered this way

set -euo pipefail

INPUT="${1:?usage: render-pdf.sh <input.html> <output.pdf>}"
OUTPUT="${2:?usage: render-pdf.sh <input.html> <output.pdf>}"

# Resolve to absolute paths — Chrome needs file:// URLs
INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
OUTPUT_ABS="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"

# Find Chrome (macOS standard locations)
CHROME=""
for candidate in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "$(which google-chrome 2>/dev/null || true)" \
  "$(which chromium 2>/dev/null || true)"; do
  if [ -n "$candidate" ] && [ -x "$candidate" ]; then
    CHROME="$candidate"
    break
  fi
done

if [ -z "$CHROME" ]; then
  echo "ERROR: No Chrome/Chromium found. Install Google Chrome from https://www.google.com/chrome/ or fall back to manual Cmd+P → Save as PDF in your browser." >&2
  exit 1
fi

# Render. --no-sandbox is fine — we're rendering a local file, no untrusted content.
"$CHROME" \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --print-to-pdf="$OUTPUT_ABS" \
  --print-to-pdf-no-header \
  "file://$INPUT_ABS" 2>/dev/null

if [ ! -f "$OUTPUT_ABS" ] || [ ! -s "$OUTPUT_ABS" ]; then
  echo "ERROR: PDF was not created or is empty." >&2
  exit 1
fi

echo "$OUTPUT_ABS"
