#!/usr/bin/env python3
"""Monte le lit musical d'une scene motion et le melange aux bruitages.

La scene porte un bloc <script type="application/json" id="music"> qui declare la
piste source et les morceaux qu'on y prend, chacun pose a une seconde du film :

  {"src": "~/Downloads/piste.mp3", "gain": 0.40,
   "crossfade": 0.05, "fade_in": 0.30, "fade_out": 1.40,
   "segments": [{"from": 19.14, "to": 27.28, "at": 0.00},
                {"from": 41.00, "to": 53.26, "at": 8.14,
                 "ramp": {"from": 0.55, "over": 3.92}}]}

Un raccord se fait sur un temps fort de la piste : le morceau entrant demarre
exactement a son "at", et c'est le morceau sortant qu'on prolonge de "crossfade"
en fondu par-dessous. L'inverse decalerait le temps fort de la duree du fondu.

Deux morceaux justes sur la pulsation peuvent quand meme s'entrechoquer si l'un
est bien plus fort que l'autre : couplet a mi-niveau suivi d'une montee en plein,
et le raccord s'entend comme une marche. "ramp" fait entrer le morceau au niveau
du precedent puis le laisse monter, ce qui rend la montee progressive au lieu de
la faire surgir. La duree se compte en mesures de la piste, pas a l'oreille.

usage: music.py <scene.html> <bruitages.wav> <sortie.wav>
"""
import json, os, re, subprocess, sys, wave
import numpy as np

SR = 48000


def decode(path):
    """La piste est decodee une fois, en stereo au format de la bande son."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32767
        return x.reshape(-1, w.getnchannels())


def ramp(n, up):
    """Fondu en puissance constante : un raccord ne creuse pas au milieu."""
    if n <= 0:
        return np.zeros(0)
    u = np.linspace(0, 1, n)
    return np.sin(u * np.pi / 2) if up else np.cos(u * np.pi / 2)


def montee(n, depart):
    """Monte de `depart` a 1 sans coin audible aux deux bouts."""
    if n <= 0:
        return np.zeros(0)
    u = np.linspace(0, 1, n)
    return depart + (1 - depart) * (u * u * (3 - 2 * u))


def main():
    scene, sfx_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    html = open(scene).read()
    # Un bloc en commentaire n'est pas declare.
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    m = re.search(r'<script type="application/json" id="music">(.*?)</script>', html, re.S)
    if not m:
        print("no music block in the scene; no music bed")
        return 1
    cfg = json.loads(m.group(1))
    dur = float(re.search(r'data-duration="([\d.]+)"', html).group(1))

    src = os.path.expanduser(cfg["src"])
    if not os.path.exists(src):
        print("music track not found: %s" % src, file=sys.stderr)
        return 2
    track = decode(src)
    xf = int(float(cfg.get("crossfade", 0.05)) * SR)

    n = int(round(dur * SR))
    bed = np.zeros((n, 2))
    for i, s in enumerate(cfg["segments"]):
        a, b = int(s["from"] * SR), int(s["to"] * SR)
        # le sortant est prolonge de crossfade, pour couvrir la couture sans
        # deplacer le temps fort du suivant
        tail = xf if i < len(cfg["segments"]) - 1 else 0
        piece = track[a:min(b + tail, len(track))].copy()
        if i > 0 and xf > 0:                      # tuer le clic d'entree, pas plus
            k = min(int(0.008 * SR), len(piece))
            piece[:k] *= ramp(k, True)[:, None]
        if tail and len(piece) > tail:
            piece[-tail:] *= ramp(tail, False)[:, None]
        r = s.get("ramp")
        if r:                                     # entrer au niveau du precedent
            m = min(int(float(r["over"]) * SR), len(piece))
            piece[:m] *= montee(m, float(r["from"]))[:, None]
        p = int(s["at"] * SR)
        k = min(len(piece), n - p)
        if k > 0:
            bed[p:p + k] += piece[:k]

    fi, fo = int(float(cfg.get("fade_in", 0.3)) * SR), int(float(cfg.get("fade_out", 1.4)) * SR)
    if fi > 0:
        bed[:fi] *= ramp(min(fi, n), True)[:, None]
    if fo > 0:
        bed[n - fo:] *= ramp(min(fo, n), False)[:, None]
    bed *= float(cfg.get("gain", 0.40))

    sfx = read_wav(sfx_path)
    if sfx.shape[1] == 1:
        sfx = np.repeat(sfx, 2, axis=1)
    k = min(len(sfx), n)
    mix = bed.copy()
    mix[:k] += sfx[:k]

    peak = np.abs(mix).max()
    if peak > 0.97:
        mix = mix / peak * 0.97
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    print("music: %d segments from %s, gain %.2f, peak %.2f -> %s"
          % (len(cfg["segments"]), os.path.basename(src), cfg.get("gain", 0.40), peak, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
