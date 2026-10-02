# motion-feature

A Claude Code skill that makes short product feature announcement videos: the product's own
interface recreated in HTML/CSS and put in motion, a scripted cursor performing the gesture,
camera moves, an end card, rendered to MP4 with its own soundtrack.

Nothing is screen-captured. That is what lets you fix one shot without reshooting, re-render
in another format, and remake the film months later when the product has moved on.

## Install

Clone it straight into the skills directory of the project where you want to use it:

```bash
git clone https://github.com/Saucemathis/motion-feature.git \
  <your-project>/.claude/skills/motion-feature
```

From a downloaded zip, unzip it into that same place. Either way the folder must be named
`motion-feature`.

Then ask Claude for a video on a feature, or type `/motion-feature`.

It can also live in `~/.claude/skills/` to be available in every project. The setup it
writes stays per project, so one install can serve several products.

## What it asks for, once

The first run holds a short intake and writes `.motion-feature/setup.md` in the project.
After that it reads that file and never asks again. Run `/motion-feature setup`, or just say
something changed, to reopen it.

1. **Where the feature is explained.** The written explanation, screenshots of the real
   screens, the exact labels, and a screen recording of the gesture when the feature is a
   tool. The recording is the piece people forget and the one that changes the film most: it
   shows what moves under the hand and everything that moves with it.
2. **The design system.** Tokens, the font files, the logo and wordmark as SVG. The film has
   to look like the product, not like a template.
3. **The background** the recreated window floats on, and the end card's ground.

## Requirements

You do not have to work these out. On its first run the skill checks the machine, tells you
what is missing and offers to install it for you. To see for yourself:

```bash
./scripts/check-setup.sh
```

It prints what is there, what is not, and the exact command for your machine, Mac with
Homebrew, Linux, or WSL on Windows, including how to get Homebrew if that is what you are
missing. What it looks for:

| Tool | What it does here |
| --- | --- |
| Google Chrome | draws every frame; the Chromium bundled with timecut is from 2020 and renders modern CSS wrong, so the system one is not optional |
| Node | runs the renderer; `npx timecut` is fetched on the first render |
| Python 3, numpy, scipy | build and filter the soundtrack |
| ffmpeg and ffprobe | assemble the frames into a video and read it back |

Chrome is found automatically on macOS, Linux and WSL. `CHROME=/path/to/chrome` overrides
the search. Windows itself is not supported directly: install WSL and work inside it.

## What is in here

| Path | What it is |
| --- | --- |
| `SKILL.md` | The procedure Claude follows: setup, material, script, build, render, trace |
| `reference/craft.md` | The rules that make these films read, with the numbers, measured on films that shipped |
| `reference/scene-template.html` | The engine: camera, cursor, timeline, readouts, text and end card, plus a worked one-click example |
| `scripts/check-setup.sh` | What this machine is missing, and the command that installs it |
| `scripts/chrome.sh` | Finds the system Chrome on macOS, Linux and WSL |
| `scripts/qc.sh` | Fixed frames from a scene, without a full render |
| `scripts/render.sh` | Frame-by-frame render to MP4, soundtrack mixed in |
| `scripts/sfx.py` | Synthesizes the sound effects the scene declares; nothing is downloaded |
| `scripts/music.py` | Cuts a music bed from a track at the seconds the scene declares |

## Try it before using it

The template renders on its own:

```bash
cd motion-feature
./scripts/check-setup.sh                                         # is anything missing
./scripts/qc.sh reference/scene-template.html 1x1 0.6 4.0 10.5   # three frames
./scripts/render.sh reference/scene-template.html 1x1            # a 12s MP4
```

If those work, the pipeline works. Then open the template: everything above the "YOUR FILM"
banner is the engine, everything below is one film's own.

## Checking a film without watching it

The scene answers questions about itself, which matters because the things that go wrong
here are invisible in a still and obvious in the video:

| Add to the URL | What it prints |
| --- | --- |
| `#t=8.4` | freezes the scene on that second |
| `#verif` | for each click, whether the cursor tip falls inside its target |
| `#speed` | the cursor's speed on screen, segment by segment, camera included |
| `#echelle` | the camera's scale every quarter second, where a zoom in followed by a zoom out shows as a peak |
| `#debug` | what share of the frame each element takes, and what each shot holds |
| `#f=16x9` | the wide cut; the square is the default |

## Credit and licence

Built from a skill used in production at Verso. The craft rules in `reference/craft.md` were
measured on the films it made, not chosen.

MIT. Use it, change it, ship what it makes.
