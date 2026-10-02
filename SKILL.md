---
name: motion-feature
description: "Produces a short product feature announcement video: the product's own UI recreated in HTML/CSS and put in motion, a scripted cursor performing the gesture, camera moves, an end card, rendered to MP4 in 1:1 and 16:9 with sound. Checks the machine has what it needs and offers to install what is missing, asks once for the feature's source material, the design system and the background, then remembers them. Triggers: 'video for feature X', 'product announcement video', 'motion design', 'feature video', '/motion-feature'."
metadata:
  version: 1.0.0
---

# Product feature video

You build a short video that shows **one** new feature in action. No voiceover, no
subtitles: the cursor and the camera tell the story. The gestures that prove the feature
set the length, usually twelve to twenty-six seconds.

The UI is **recreated in HTML/CSS**, never screen-captured. That is what lets you control
timing to the frame, fix one shot without reshooting, re-render in another format, and
remake the film six months later when the product has moved on.

[`reference/craft.md`](reference/craft.md) holds the rules that make these films read:
framing, cursor, camera, typing, sound, and the measurements that catch what the eye
misses. Read it before writing anything. This file holds the procedure.

## Step 0a — check the machine can render, before anything else

Films are rendered by tools that live outside this folder: Node, Python with numpy and
scipy, ffmpeg, and Google Chrome. **Run `scripts/check-setup.sh` at the start of the first
run in a project**, before the intake, and again whenever a render fails with a missing
command. It is silent when everything is there.

If something is missing, it prints every missing piece at once and the exact command for
this machine, macOS with Homebrew, Linux or WSL, including how to get Homebrew when that
is what is missing. Then:

1. **Show the person what is missing and what it is for**, in their language, in a line or
   two. Not a terminal dump: "ffmpeg assembles the frames into a video, and it is not on
   your machine."
2. **Offer to install it, and say what the command will do.** Installing software on
   someone's computer is their decision, not yours, and a non-developer cannot judge a
   command they did not ask for. Ask once, plainly: may I install these.
3. **On yes, run it and report the result.** On no, give them the command to run
   themselves and stop: there is no film without these.
4. **Homebrew is its own step.** Its installer asks for the Mac password and prints two
   lines to paste so that `brew` is found afterwards. You cannot type the password for
   them, so hand them the command, say what it will ask, and wait.

Never install anything without that yes, and never work around a missing tool by
rendering at lower quality or skipping the sound.

## Step 0b — setup, asked once

Three things do not change from one film to the next, and the film is only as good as
they are. Ask for them **once**, write them down, and never ask again.

**At the start of every run, read `.motion-feature/setup.md` from the working directory.**
If it exists, use it and say nothing. If it is missing, hold the intake conversation below
and write the file. If the user types `/motion-feature setup`, or says something changed,
reopen it and edit the file rather than starting over.

Ask the three in one message, in the user's language, and explain what each one buys. A
user who understands why a screen recording matters sends one; a user who is only asked
for "materials" sends a screenshot.

### 1. Where the feature is explained

Ask for the source of truth on what the feature does and why it matters. Then say plainly
what makes the film accurate, and what each piece prevents:

- **A written explanation** (a release note, a spec, a changelog entry): what the feature
  does, who it is for, and the sentence the film should end on.
- **Screenshots of the real screens**, at full width. They give the layout, the spacing and
  the hierarchy that no description conveys.
- **The exact labels and states**, from the component code if there is access to it, or
  from the screenshots read carefully. Marketing material shows mockups that were never
  shipped; a film that invents a button is worse than no film.
- **A screen recording of the gesture**, whenever the feature is a tool rather than a
  state. It is the one piece people forget and the one that changes the film most: it
  shows what moves under the hand, and everything that moves *with* it. A single drag can
  update four numbers elsewhere on the page, and none of that is visible in a screenshot.

Say it in those terms: without the recording and the real labels, the film will show a
feature that looks plausible and does not match the product.

### 2. The design system

The film has to look like the product, not like a template.

- **Tokens**: the colour scale, the typefaces and their weights, radii, shadows, spacing.
  A CSS file or a tokens export is ideal; a screenshot plus a hex list works.
- **The fonts themselves**, as files. They are embedded in the scene as base64 so no frame
  ever renders without the typeface.
- **The logo and the wordmark**, as SVG, for the end card.

Record where each lives, so a later run picks it up without asking.

### 3. The background the feature is shown on

The recreated window floats on something, and that something is half the look.

- A gradient, a flat colour, an image, or the product's own marketing ground.
- Whether the end card shares it or has its own.

If the user has no preference, propose one and record what was chosen, so the second film
matches the first.

### What to write

`.motion-feature/setup.md`, in the working directory, created by this step:

```markdown
# motion-feature setup

Written <date>. Edit this file or run `/motion-feature setup` when something changes.

## Machine
Checked on <date>: everything `scripts/check-setup.sh` asks for is installed.
<or: what is missing and what the person decided about it>

## Source of the feature explanation
<where the written explanation lives, and how to get at it>
<where screenshots come from; who to ask>
<whether the component code is reachable, and where>
<how screen recordings arrive>

## Design system
Tokens: <path or url>
Fonts: <path to the files>
Logo and wordmark: <path to the SVG>

## Background
<what the window floats on, and the end card's ground>

## Conventions
Productions: <folder>/<slug>/ holding script.md and scene.html
Renders: <folder, outside the repository>
```

Show the file once, then get on with the film.

## Step 1 — gather this feature's material

With the setup in hand, collect for **this** feature what step 0 said to expect: the
written explanation, the screenshots, the real labels, and a recording of the gesture if
it is a tool. Ask for whatever is missing, naming it precisely.

Two more, when they apply:

- **A recording of a person**, if the feature plays one. Stock footage reads as stock;
  [craft.md](reference/craft.md#a-stock-person-does-not-look-like-a-real-recording) says
  what a real one looks like and what it costs.
- **The music track.** It is an input, not a finish: the film's beats are written on its
  bar. Pick one with a steady bar the whole film can sit on, and two or three identifiable
  hard points, a re-entry, a build, a last hit, to hang the opening, the gesture that
  carries the argument and the logo on.

If the written explanation and the real screens disagree, **flag it** in the script
proposal rather than deciding silently.

## Step 2 — propose the script, and wait

**The grid comes before the table.** Neither you nor the user can read a rhythm from a
column of seconds, so write every beat at a multiple of the track's bar from the start:
the clicks then land on downbeats by construction instead of being corrected onto them,
and a beat added in review moves the film by a bar instead of drifting it.

A shot table: number, time, what's on screen, camera move. Rules:

- **One feature, one gesture.** Open, choose, see the result. If you need three gestures,
  that is three videos.
- **The film opens before it moves.** The window at rest, legible, no approach begun, for
  its whole opening beat: the viewer places the screen before being taken anywhere.
- **The approach to a control is a step closer, not a close-up.** The control has to stay
  readable as part of the page it sits on.
- **Show the gesture, not its result.** A feature that lets someone change something is
  proved by the change happening under the cursor, with every number that depends on it
  moving at the same time. Showing the editor is not showing that it edits.
- **An input the user fills starts empty and fills itself letter by letter.**
  [craft.md](reference/craft.md#an-input-fills-itself-letter-by-letter) owns the rate and
  what to do when the real text is too long.
- The beat that carries the argument, the line that proves it or the number that changes,
  deserves a slightly tighter framing and a two-second pause.
- **Hold the last interface shot longer than feels necessary**, so the changed state can be
  read. It always looks long in the table and short in the film.
- The end card reprises the feature's name in the source material's own words.

**Propose the square first** when the film is for a feed. It is framed *wider* than the
16:9, not tighter;
[craft.md](reference/craft.md#the-square-is-not-a-crop-of-the-169-and-it-is-framed-wider)
owns why.

**You build nothing until the user has approved the script.** This is the step where an
iteration costs a minute, versus an hour after the build.

Anonymize every customer datum on screen and say so in the proposal: names, brands,
figures, quotations. If a real recording plays, list its consent in the script's "To verify
before publication", next to the music licence.

## Step 3 — build the scene

Start from [`reference/scene-template.html`](reference/scene-template.html). It carries the
engine, the readouts and a worked one-click example; the product's UI is yours to build
from the design system and the screenshots.

One production = one folder `<productions>/<slug>/` with `script.md`, the approved script,
and `scene.html`.

The scene contract, to respect:

| Rule | Why |
| --- | --- |
| `<body data-duration data-fps>` is the single source of truth | `render.sh` reads the duration and fps from it, nothing to re-enter |
| A single timeline driven by render time (`requestAnimationFrame`) | Reproducible to the frame, unlike CSS animations |
| Anchors for the cursor and camera are **measured** on the real elements via `getBoundingClientRect` | A hardcoded coordinate breaks at the first layout change |
| Zooms are written in **visible world width**, not a scale factor | The same move reads correctly in every format |
| Hover is computed by testing the cursor position against the elements | You get real-pointer behaviour, including the rows it crosses |
| Fonts embedded as base64 | No network call at render time, so no frame without the typeface |
| `#t=<seconds>` freezes the scene on a frame | Lets you check a shot without rendering the video |
| `#speed` shows the cursor speed segment by segment, on its **screen** path | Speed is tuned by the number, and a camera moving with or against the gesture changes it |
| `#verif` prints, for each click, where the cursor tip falls inside its target | A click beside its button does not show in the code and barely shows in a still |
| `#echelle` prints the camera scale every quarter second | A zoom in followed by a zoom out reads as a peak in that column, where the eye expects one breath |
| `#debug` prints the framing: what share of the frame each element takes | Framing is checked by the number before it is checked by eye |
| Sound effects declared in a JSON block `id="sfx"` | Sound follows the edit instead of being timed by hand |
| A music bed declared in a JSON block `id="music"`: the track, and which pieces of it are laid at which second | One source of truth, and the same cut re-renders from any copy of the track |

## Step 4 — render and check

```bash
scripts/check-setup.sh                        # is this machine able to render
scripts/qc.sh <scene.html> 1x1 0.5 4.8 8.6    # fixed frames, no full render
scripts/render.sh <scene.html> 1x1            # MP4 with its soundtrack
scripts/render.sh <scene.html> 16x9
```

The square goes first when the film is for a feed: it is the format that ships, and a
correction found on it is cheaper before the wide one is rendered.

`render.sh` mixes the soundtrack if the scene declares an `sfx` block; `sfx.py` synthesizes
it, with no external sample. Without that block the video comes out silent. If the scene
also declares a `music` block, `music.py` cuts the bed from the track and lays the sound
effects over it. [craft.md](reference/craft.md#cut-the-film-to-the-track) owns how the film
is cut to the music.

The readouts avoid judging by eye, which matters when you cannot see the images: `#speed`,
`#debug`, `#echelle`, `#verif`.

**Rerun `#verif` after any change to what is on screen, not only to the cursor path.** An
element that replaces another is measured where it will actually be, with the one it
replaces hidden. Measured underneath it, a card read a whole card too low and the click
landed beside its button, which the still at that second almost hid.

**Check the rendered MP4, not the page**: extract every frame and read the mean difference
between consecutive ones. No frame without content, no seam, and no held run nobody asked
for; [craft.md](reference/craft.md#the-easing-itself-creates-the-frozen-shots) says what the
runs mean. A shot framed crooked does not show in the code either, only in the image.

Renders go to the folder the setup names, never into a repository: keep the sources, not
the binaries.

## Step 5 — leave a trace

What remains must be enough for someone else to redo one:

1. `script.md` in the production folder: the approved shot table, the decisions taken and
   why, the music edit written as timecodes so it reproduces from any copy of the track,
   and a "To verify before publication" list.
2. If the run learned something reusable, write it down where that kind of rule lives, in
   one place only: craft, framing, timing and their numbers in
   [`reference/craft.md`](reference/craft.md); procedure, what to gather and what to check,
   here. A rule written in both drifts, and the copy the next reader finds is the wrong one.

## Known pitfalls

- **`--executable-path` pointing at the system Chrome is mandatory** in `render.sh`. The
  Chromium bundled with timecut 0.3.3 dates from 2020: without it, modern CSS breaks and
  colours and centring come out wrong. `chrome.sh` finds it on macOS, Linux and WSL;
  `CHROME=/path/to/chrome` overrides the search.
- **No `--threads`**: multi-threading crashes on the temp folders.
- **`--start-delay 3`** at minimum, otherwise the first frames film a page that has not
  settled.
- An element measured through a transform, a closed state or another element stacked above
  it gives a wrong box, and the camera then frames empty space. Neutralize the transform,
  show the element, hide what it replaces, measure once, restore.
- A list longer than its container overflows it silently. Anchor a popover by computing
  that it fits, the way a real one would.
