#!/usr/bin/env bash
# Extrait des frames fixes d'une scene, sans passer par un rendu complet.
# usage: qc.sh <scene.html> <16x9|1x1|9x16> <t1> [t2 ...]
set -euo pipefail
source "$(dirname "$0")/chrome.sh"

SCENE_PATH=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
FMT=$2; shift 2
case "$FMT" in
  16x9) VP="1920,1080" ;;
  1x1)  VP="1080,1080" ;;
  9x16) VP="1080,1920" ;;
esac
OUTDIR=${QC_DIR:-./qc}
mkdir -p "$OUTDIR"

for T in "$@"; do
  "$(chrome_or_die)" \
    --headless --disable-gpu --hide-scrollbars \
    --window-size="${VP/,/,}" \
    --virtual-time-budget=2500 \
    --screenshot="${OUTDIR}/${FMT}-t${T}.png" \
    "file://${SCENE_PATH}#f=${FMT}&t=${T}" 2>/dev/null
  echo "${OUTDIR}/${FMT}-t${T}.png"
done
