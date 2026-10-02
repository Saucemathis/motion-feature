#!/usr/bin/env python3
"""Fabrique la bande son d'une scene motion, a partir des reperes qu'elle declare.

La scene porte un bloc <script type="application/json" id="sfx"> avec ses cues, ce
qui garde une seule source de verite : si le montage bouge, le son suit.

usage: sfx.py <scene.html> <sortie.wav>
"""
import json, re, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

SR = 48000

def band(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], btype="band")
    return lfilter(b, a, x)

def noise(n, seed):
    return np.random.default_rng(seed).normal(0, 1, n)

def env(n, attack, release):
    """Enveloppe attaque/chute, en secondes."""
    a, r = max(int(attack * SR), 1), max(int(release * SR), 1)
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a)
    if r < n:
        e[n - r:] = np.linspace(1, 0, r) ** 1.8
    return e

# --- clics : trois recettes, la plus simple par defaut ---------------------
def click_sec(seed=0):
    """Le clic le plus simple possible : une seule transitoire de bruit, 6 ms."""
    n = int(0.006 * SR)
    x = band(noise(n, seed), 2000, 9000)
    return x / (np.abs(x).max() + 1e-9) * np.exp(-np.arange(n) / SR * 700) * 0.55

def click_feutre(seed=0):
    """Variante ronde : un petit tock mat, sans souffle."""
    n = int(0.016 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 900 * t) * np.exp(-t * 320)) * 0.5

def click_mecanique(seed=0):
    """Variante mecanique : l'appui, puis le relachement du bouton."""
    n = int(0.075 * SR)
    out = np.zeros(n)
    d = click_sec(seed)
    out[:len(d)] += d
    up = click_sec(seed + 1)[: int(0.004 * SR)] * 0.45
    p = int(0.055 * SR)
    out[p:p + len(up)] += up
    return out

CLICKS = {"sec": click_sec, "feutre": click_feutre, "mecanique": click_mecanique}

def blip(f0, f1, dur, amp, seed):
    """Petit son d'interface, balaye doucement en frequence."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph)
    return s * env(n, 0.004, dur * 0.8) * amp

# --- souffles de camera : court et discret, il marque le depart du mouvement,
#     il ne l'accompagne pas d'un bout a l'autre ------------------------------
def whoosh_court(dur=0.30, amp=0.055, seed=0):
    n = int(dur * SR)
    x = band(noise(n, seed), 250, 1200)
    shape = np.sin(np.linspace(0, np.pi, n)) ** 1.4
    return x / (np.abs(x).max() + 1e-9) * shape * amp

def whoosh_bref(dur=0.17, amp=0.045, seed=0):
    n = int(dur * SR)
    x = band(noise(n, seed), 400, 2200)
    shape = np.sin(np.linspace(0, np.pi, n)) ** 1.2
    return x / (np.abs(x).max() + 1e-9) * shape * amp

def whoosh_montant(dur=0.38, amp=0.055, seed=0):
    """Attaque franche puis chute : on entend le depart du mouvement."""
    n = int(dur * SR)
    x = band(noise(n, seed), 200, 1600)
    shape = np.concatenate([np.linspace(0, 1, int(n * 0.25)) ** 0.6,
                            np.linspace(1, 0, n - int(n * 0.25)) ** 1.8])
    return x / (np.abs(x).max() + 1e-9) * shape * amp

WHOOSHES = {"court": whoosh_court, "bref": whoosh_bref, "montant": whoosh_montant}

def swell(dur, amp, seed):
    """Arrivee du carton de fin : une nappe grave, tres discrete."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 110 * t) * 0.6 + np.sin(2 * np.pi * 165 * t) * 0.3
         + np.sin(2 * np.pi * 220 * t) * 0.15)
    air = band(noise(n, seed), 300, 2500) * 0.12
    return (s + air) * env(n, dur * 0.45, dur * 0.5) * amp

CLICK_KIND = "mecanique"
WHOOSH_KIND = "bref"

def audition(outdir):
    """Ecrit un echantillon par recette, pour choisir a l'oreille avant de monter."""
    import os
    os.makedirs(outdir, exist_ok=True)
    def write(path, x):
        st = np.stack([x, x], axis=1)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
        print(path)
    gap = np.zeros(int(0.45 * SR))
    for name, fn in CLICKS.items():
        seq = np.concatenate([np.concatenate([fn(i), gap]) for i in range(3)])
        write("%s/clic-%s.wav" % (outdir, name), seq)
    for name, fn in WHOOSHES.items():
        # deux souffles, puis un clic : on juge aussi l'equilibre entre les deux
        seq = np.concatenate([fn(seed=0), gap, fn(seed=1), gap, click_sec(0), gap])
        write("%s/camera-%s.wav" % (outdir, name), seq)

def main():
    if sys.argv[1] == "--audition":
        audition(sys.argv[2]); return 0
    scene, out = sys.argv[1], sys.argv[2]
    html = open(scene).read()
    # Un bloc en commentaire n'est pas declare.
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    m = re.search(r'<script type="application/json" id="sfx">(.*?)</script>', html, re.S)
    if not m:
        print("no sfx block in the scene; no soundtrack generated")
        return 1
    cues = json.loads(m.group(1))["cues"]
    dur = float(re.search(r'data-duration="([\d.]+)"', html).group(1))

    buf = np.zeros(int((dur + 0.5) * SR))
    for i, c in enumerate(cues):
        k = c["k"]
        if k == "click":      x = CLICKS[CLICK_KIND](i)
        elif k == "pop":      x = blip(520, 820, 0.10, 0.24, i)
        elif k == "popclose": x = blip(760, 470, 0.09, 0.16, i)
        elif k == "whoosh":   x = WHOOSHES[WHOOSH_KIND](seed=i)
        elif k == "endcard":  x = swell(1.60, 0.16, i)
        else:                 continue
        p = int(c["t"] * SR)
        n = min(len(x), len(buf) - p)
        if n > 0:
            buf[p:p + n] += x[:n]

    # Niveaux absolus, pas de normalisation globale : baisser un son doit vraiment
    # le baisser, et non remonter tous les autres.
    peak = np.abs(buf).max()
    if peak > 0.9:
        buf = buf / peak * 0.9
    st = np.stack([buf, buf], axis=1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("soundtrack: %s (%.1fs, %d cues)" % (out, dur, len(cues)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
