#!/usr/bin/env bash
# Trouve le Chrome du systeme. Sourced par render.sh et qc.sh.
#
# Le chemin ne peut pas etre ecrit en dur : il differe entre macOS, Linux et WSL,
# et une personne qui n'ecrit pas de code ne corrigera pas un script pour cela.
# CHROME=/chemin/vers/chrome force le choix.

find_chrome() {
  if [ -n "${CHROME:-}" ]; then
    [ -x "$CHROME" ] && { echo "$CHROME"; return 0; }
    echo "CHROME is set to a file that cannot be run: $CHROME" >&2
    return 1
  fi
  local c
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
  do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return 0; }
  done
  return 1
}

chrome_or_die() {
  local p
  if ! p=$(find_chrome); then
    echo "Google Chrome not found." >&2
    echo "Run scripts/check-setup.sh: it says what is missing and how to install it." >&2
    exit 3
  fi
  echo "$p"
}
