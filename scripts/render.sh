#!/usr/bin/env bash
# Rend une scene motion en MP4, frame par frame, via timecut.
# usage: render.sh <scene.html> [16x9|1x1|9x16] [sortie.mp4]
set -euo pipefail

SCENE_PATH=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
FMT=${2:-16x9}
case "$FMT" in
  16x9) VP="1920,1080" ;;
  1x1)  VP="1080,1080" ;;
  9x16) VP="1080,1920" ;;
  *) echo "format inconnu: $FMT (16x9|1x1|9x16)"; exit 1 ;;
esac

# La duree et le fps sont declares sur <body>, une seule source de verite.
DUR=$(grep -o 'data-duration="[0-9.]*"' "$SCENE_PATH" | head -1 | grep -o '[0-9.]*')
FPS=$(grep -o 'data-fps="[0-9]*"' "$SCENE_PATH" | head -1 | grep -o '[0-9]*')
BASE=$(basename "${SCENE_PATH%.html}")
OUT=${3:-"$HOME/Downloads/${BASE}-${FMT}.mp4"}

# Un bloc JSON mis en commentaire n'est pas declare : on cherche donc les blocs
# apres avoir retire les commentaires HTML, sinon l'exemple commente du modele
# declencherait le mixage.
bloc_declare() {
  python3 - "$SCENE_PATH" "$1" <<'PY'
import re, sys
html = re.sub(r'<!--.*?-->', '', open(sys.argv[1], encoding='utf-8').read(), flags=re.S)
sys.exit(0 if re.search(r'id="%s"' % sys.argv[2], html) else 1)
PY
}

# La piste musicale se verifie avant le rendu : la trouver absente apres huit
# cents frames coute le rendu entier pour une erreur connue d'avance.
if bloc_declare music; then
  PISTE=$(python3 - "$SCENE_PATH" <<'PY'
import json, os, re, sys
html = re.sub(r'<!--.*?-->', '', open(sys.argv[1], encoding='utf-8').read(), flags=re.S)
cfg = json.loads(re.search(r'id="music">(.*?)</script>', html, re.S).group(1))
print(os.path.expanduser(cfg["src"]))
PY
)
  if [ ! -f "$PISTE" ]; then
    echo "piste introuvable: $PISTE" >&2
    echo "corrige le \"src\" du bloc music de la scene, ou commente le bloc." >&2
    exit 2
  fi
fi

echo "rendu ${BASE} ${FMT} ${VP} ${DUR}s @${FPS}fps -> ${OUT}"

# --executable-path : le Chromium embarque par timecut 0.3.3 date de 2020 et ne
#   sait pas rendre le CSS moderne. Sans ca, couleurs et centrage sont faux.
# --start-delay : laisse la page se poser (fonts, layout) avant la premiere frame.
# Pas de --threads : le multi-thread plante sur les dossiers temporaires.
SILENT="${TMPDIR:-/tmp}/${BASE}-${FMT}-silent.mp4"
npx timecut "file://${SCENE_PATH}#f=${FMT}" \
  --viewport "$VP" \
  --executable-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --start-delay 3 \
  --fps "$FPS" \
  --duration "$DUR" \
  --output "$SILENT"

# La scene declare ses bruitages : on les synthetise et on les mixe. Pas de bloc
# sfx, pas de bande son, et la video sort muette comme avant.
if bloc_declare sfx; then
  WAV="${TMPDIR:-/tmp}/${BASE}-sfx.wav"
  python3 "$(dirname "$0")/sfx.py" "$SCENE_PATH" "$WAV"
  # La scene peut aussi declarer un lit musical : les morceaux qu'on prend dans la
  # piste sont poses aux secondes du film, et les bruitages viennent par-dessus.
  if bloc_declare music; then
    MIX="${TMPDIR:-/tmp}/${BASE}-mix.wav"
    python3 "$(dirname "$0")/music.py" "$SCENE_PATH" "$WAV" "$MIX"
    rm -f "$WAV"; WAV="$MIX"
  fi
  ffmpeg -v error -y -i "$SILENT" -i "$WAV" -map 0:v -map 1:a \
    -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
  rm -f "$SILENT" "$WAV"
else
  mv "$SILENT" "$OUT"
fi

echo "ok: $OUT"
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate \
  -of default=noprint_wrappers=1 "$OUT"
