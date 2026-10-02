#!/usr/bin/env bash
# Dit en une fois tout ce qui manque pour rendre un film, et la commande exacte
# qui l'installe sur cette machine.
#
# Sort 0 si tout est la, 1 s'il manque quelque chose. L'agent lit "MISSING:" pour
# savoir quoi proposer d'installer; la personne lit le reste.
# usage: check-setup.sh [--quiet]
set -uo pipefail
cd "$(dirname "$0")"
source ./chrome.sh

QUIET=${1:-}
MISSING=()
ok(){ [ "$QUIET" = "--quiet" ] || printf '  \033[32mok\033[0m    %s\n' "$1"; }
no(){ [ "$QUIET" = "--quiet" ] || printf '  \033[31mmiss\033[0m  %s\n' "$1"; MISSING+=("$2"); }

case "$(uname -s)" in
  Darwin) OS=mac ;;
  Linux)  grep -qi microsoft /proc/version 2>/dev/null && OS=wsl || OS=linux ;;
  *)      OS=other ;;
esac

[ "$QUIET" = "--quiet" ] || echo "Checking what this machine has:"

command -v node >/dev/null  && ok "Node $(node -v)"            || no "Node (runs the renderer)" node
command -v npx  >/dev/null  && ok "npx"                        || no "npx (comes with Node)" node
command -v python3 >/dev/null && ok "Python $(python3 -V 2>&1 | cut -d' ' -f2)" || no "Python 3" python
command -v ffmpeg  >/dev/null && ok "ffmpeg"                   || no "ffmpeg (assembles the video)" ffmpeg
command -v ffprobe >/dev/null && ok "ffprobe"                  || no "ffprobe (comes with ffmpeg)" ffmpeg

if command -v python3 >/dev/null; then
  python3 -c "import numpy" 2>/dev/null && ok "numpy"          || no "numpy (Python, builds the sound)" numpy
  python3 -c "import scipy" 2>/dev/null && ok "scipy"          || no "scipy (Python, filters the sound)" scipy
fi

if CH=$(find_chrome); then ok "Chrome ($CH)"; else no "Google Chrome (draws every frame)" chrome; fi

if [ ${#MISSING[@]} -eq 0 ]; then
  [ "$QUIET" = "--quiet" ] || echo "Everything needed is here. Nothing to install."
  exit 0
fi

# Une commande par gestionnaire, pas une par outil : une personne qui n'ecrit pas
# de code en colle une, pas cinq. Et --cask ne se melange pas aux formules, donc
# Chrome a sa propre ligne.
BREW=() CASK=() APT=() PIP=() LINKS=()
for m in "${MISSING[@]}"; do
  case "$m" in
    node)   BREW+=(node);   APT+=(nodejs npm) ;;
    python) BREW+=(python); APT+=(python3 python3-pip) ;;
    ffmpeg) BREW+=(ffmpeg); APT+=(ffmpeg) ;;
    numpy)  PIP+=(numpy) ;;
    scipy)  PIP+=(scipy) ;;
    chrome) CASK+=(google-chrome); APT+=(chromium-browser)
            LINKS+=("Or download Chrome itself: https://www.google.com/chrome/") ;;
  esac
done
dedup(){ printf '%s\n' "$@" | awk '!seen[$0]++' | paste -sd' ' -; }

CMDS=()
case "$OS" in
  mac)
    [ ${#BREW[@]} -gt 0 ] && CMDS+=("brew install $(dedup "${BREW[@]}")")
    [ ${#CASK[@]} -gt 0 ] && CMDS+=("brew install --cask $(dedup "${CASK[@]}")")
    ;;
  linux|wsl)
    [ ${#APT[@]} -gt 0 ] && CMDS+=("sudo apt update && sudo apt install -y $(dedup "${APT[@]}")")
    ;;
esac
[ ${#PIP[@]} -gt 0 ] && CMDS+=("python3 -m pip install --user $(dedup "${PIP[@]}")")

echo
N=$(dedup "${MISSING[@]}" | wc -w | tr -d ' ')
if [ "$N" = 1 ]; then echo "One thing is missing. To install it, run:"
else echo "$N things are missing. To install them, run:"; fi
echo

if [ "$OS" = other ]; then
  echo "  This machine is neither macOS nor Linux. On Windows, install WSL"
  echo "  (Windows Subsystem for Linux), then reopen the project inside it:"
  echo
  echo "    wsl --install"
  echo
  echo "  Chrome installed on Windows is found automatically from WSL."
elif [ "$OS" = mac ] && ! command -v brew >/dev/null; then
  echo "  Homebrew is missing. It is how a Mac installs tools like these, and"
  echo "  everything else needs it. Paste this in Terminal and follow its prompts:"
  echo
  echo '    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo
  echo "  It asks for your Mac password, and may ask to install Apple's command"
  echo "  line tools, which is expected. It then prints two lines to paste so the"
  echo "  brew command is found; do that, then run:"
  echo
  for c in "${CMDS[@]}"; do echo "    $c"; done
else
  for c in "${CMDS[@]}"; do echo "    $c"; done
  [ "$OS" = wsl ] && echo "    (Chrome installed on Windows is found automatically)"
fi
# Sur Windows la personne doit d'abord passer par WSL : lui donner un lien de
# telechargement a ce moment la l'enverrait dans le mur.
if [ "$OS" != other ]; then
  for l in ${LINKS+"${LINKS[@]}"}; do echo "    $l"; done
fi

echo
echo "MISSING: $(dedup "${MISSING[@]}")"
exit 1
