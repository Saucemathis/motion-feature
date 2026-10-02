# Craft rules

What makes these films read. Procedure lives in [SKILL.md](../SKILL.md); this file owns the
rules, the numbers and the measurements. Every figure here was measured on a film that
shipped, not chosen.

## The grammar

The UI is a card floating on a background, with rounded corners, a large soft shadow and
generous margins. The card is the subject; the background is coloured empty space.

An oversized, scripted cursor performs the gesture: it glides with easing, hovers, triggers
hover states, clicks. It lives in the card's space, so it grows with the zoom.

No overlay text during the demonstration. No subtitles, no arrows, no "New!". If the
gesture does not make sense on its own, the script is wrong.

| Moment | Framing | Indicative duration |
| --- | --- | --- |
| Opening, screen at rest | Full card, held still, then the push-in begins | about 1s held, 1.5 to 2s in all |
| Approach to the control | A step closer, cursor enters the frame | 1.5s |
| The gesture: opening, typing, dragging | Medium framing on the active area | 2 to 2.5s |
| The argument: the line that proves it | Same framing, pause | 2s |
| The result | Zoom-out begins, changed state visible | 1.5s |
| Return to the wide shot | The opening framing | 1.5 to 2s |
| End card | Full frame | 1.5 to 2s |

These are indicative. A film with one gesture lands near twelve seconds; one with three
needs twice that. A beat held because the grid had room for it is padding.

## Starting distance

The opening shot is far away: the card takes about 87% of the frame width and 70 to 73% of
its height in 16:9, centred, with the vertical margins about twice the horizontal ones. A
card filling more than 80% of the height feels cramped even when perfectly centred:
vertical margin creates distance, not centring.

Framing is calculated from the card's actual width plus a margin, never from a hardcoded
scale factor.

## The square is not a crop of the 16:9, and it is framed wider

A camera written in visible world width reads alike in both formats only while the shot
holds one object. As soon as it has to hold two, a card and a drawer side by side, the
square fails: it is half as wide, so the same world width halves everything on screen and
interface text lands at eight pixels. Either the shot is rewritten for the square, which
then pays a pan the 16:9 does not need, or the square is not delivered.

**The answer is not to zoom in until the text is legible.** That is the first instinct and
it is wrong. A square runs in a feed, on a phone, where 1080 pixels become about four
hundred: no interface label survives that, whatever the scale. So the square is composed
for the gesture and the 16:9 for the page. Its shots keep the whole window height in frame,
around 0,70 to 0,90 where the 16:9 goes to 1,12 and beyond, and the viewer sees what is
being done rather than deciphering what is written.

Full-frame text is the easy case and already followed this: a phrase fills 0,76 of the
square's width against 0,60 of the wide one, because a phrase can be scaled to its frame
and a screenshot cannot.

## A shot cannot hold what is wider than its window

Before tuning a framing by eye, compare the element's width against the world width the
shot shows. A row 1636 wide in a shot showing 1300 loses 168 pixels at each end, and those
are the ends that carry the label and the badge, so the result of the gesture arrives
unreadable. Centring on the element does not help: it cuts both sides instead of one.

The answer is usually the layout, not the camera. Real interfaces cap their content width
and centre it; a recreation that lets a row run the full width of a 2000-pixel window has
invented a page no product ships, and no square frame can hold it. Cap the content, then
check the number: for each keyframe, the world window it shows and the share of the target
inside it. `#debug` prints both, and a shot holding less than all of its subject is a
framing error the still at that second will not make obvious.

## A window shorter than the frame caps the zoom

A window 940 high inside a 1080 frame can only be zoomed past about 1,15 by giving up the
freedom to place it: beyond that the frame is shorter than the window, and an element stuck
to its top or bottom, an action bar or an input bar, cannot be centred without uncovering
the background. So the tight framings go to the elements at mid-height, which happen to be
the ones carrying the argument, and the beats aiming at an edge stay soft.

Write it as a function, not as judgement: pull each keyframe back inside the window for the
scale it asks for, once, when the camera is built. Chosen by eye, the same framing silently
shows a band of background under the interface.

## Smooth camera movement

Judge a zoom by its scale factor per second. Above 2x per second it feels violent even with
a good curve. Aim for 1,4x at most, and remove transitions rather than speed them up: two
smooth moves beat three fast ones.

Return to the wide shot in **one** movement, with no intermediate step. Passing through a
medium framing before opening creates two accelerations where the eye expects one breath.
The same applies across a cut: tightening onto something and then pulling straight back out
reads as a peak. Sample the camera's scale over time and look at the curve.

A camera that stays still while a gesture plays is doing its job.

## The easing itself creates the frozen shots

The rule that a camera must never stop is not only about writing a still beat. Between two
keyframes an ease-in-out brings the speed back to zero at both ends, so every pause in the
gesture, and every keyframe placed mid-shot to shape a push-in, lands on a passage the eye
reads as a photograph. On one pass of a film, fourteen passages measured a frame-to-frame
difference under 0,05 and one lasted 1,2 seconds.

**A slow global drift does not fix this, and measuring proves it.** One percent of scale
across a 22-second film moves the frame edge by less than a hundredth of a pixel per image:
the number does not move, and neither does the picture. A drift only reads when it is large
enough to be a camera move, which is not what a resting shot wants.

What fixes it is having something to watch. Remove the mid-shot keyframe so a push-in is one
continuous ease. Start the cursor before the stretch rather than after it. Let a streaming
answer arrive word by word instead of as a block, which is also how it really arrives. And
above all, do not hold the bare background: the worst passage of one film was the second and
a half between the window fading out and the first word of the closing card, and the cure was
to move the window's exit one bar later, not to animate the gradient.

A hold that carries a gesture is not this defect. A third of a second on a target before a
click is what the style asks for; the closing card and the logo hold on purpose; and so does
the opening, where the window is held still for about a second before any approach begins,
because the viewer has to place the screen before being taken anywhere. Read the runs, not
the count.

## The cursor

The tip is at the cursor's upper left, but the eye reads the arrow's body. Aiming at an
element's geometric centre therefore makes a click read **below** the element. Aim in the
upper third and past the icon, around 40% of the width and 35 to 45% of the height, and test
hover with the tip position, so the highlighted row is the one the arrow covers.

Aim at the element being acted on, not the row containing it. The middle of a wide row lands
beside the checkbox at its edge.

**A cursor does not disappear; it leaves the frame.** Fading it in place looks like a cut.

**Everything that opens must have been clicked, and everything that closes must have been
clicked too.** A menu that opens without a visible click, or closes by itself, breaks the
reading of the gesture. Every click gets a pulse: without it, we see the cursor pass, not
act.

### Measuring, and the traps

**Neutralize every transform before measuring, not just the camera's.** A window has its own
transform during its entrance: measuring an element then gives a position offset by the whole
entrance. The symptom is dramatic, the camera frames empty space, and a check on a frozen
frame mid-shot misses it, because the transforms are the identity by then. The test that
catches it is to measure at two moments and compare.

**Measure before starting entrances.** An element just revealed still carries its entrance
offset: measured then, it is about ten pixels out.

**Measure targets once, with the camera neutralized.** `getBoundingClientRect` returns screen
coordinates, already transformed by the camera. Measuring every frame uses screen coordinates
as scene coordinates: the cursor drifts as the camera moves and lands on nothing. The trap is
subtle because the camera is still neutral on the first frame, so a check that looks only at
that frame says everything is fine.

**An element that replaces another is measured in its own final position**, with the one it
replaces hidden. Measured while both are laid out, a result card read a whole card too low
and the click landed beside its button.

`#verif` compares, for each click, the cursor tip against its target. Rerun it after any
change to what is on screen, not only to the cursor path.

## Cursor speed

Measured on real reference footage: pointing moves sit between **350 and 450 px/s on
screen**, entries and exits rise toward 1100. Below 300 the gesture drags; above 600 it
becomes nervous and hard to read. A deliberate gesture, dragging a handle, is slower on
purpose and reads fine near 200.

**Read the speed where the viewer sees it**, on the cursor's screen path with the camera
included. World distance multiplied by camera scale is only right while the camera is still:
when it moves with the gesture that figure overstates the speed, when it moves against it,
it understates it, and two gestures written the same way come out at 418 and 797 px/s. The
staging consequence is a rule: a long gesture is cheap when the camera travels with it and
expensive when it travels against it, so aim the camera where the cursor is going.

Two more:

- The cursor is **already in the frame** in the opening shot. Bringing it in from outside
  costs a long path, which means a rushed entrance or two seconds lost.
- A path through a list uses **one** segment, never intermediate steps: every waypoint adds a
  deceleration and then an acceleration, which reads as hesitation.

## An input fills itself letter by letter

A box the user is supposed to fill starts empty, stays empty for about half a second so that
state is seen, and then writes itself one character at a time. A block of text appearing at
once is not someone writing, and the viewer reads it as a box that was already full. This
holds even against the product: on one film the page really does hand the field a pre-filled
draft, the film reproduced that exactly, and it was sent back twice.

**The rate is the constraint, so the text gives way to it.** Measured: 59 characters over
1,66s, about 36 a second, which is fast and still a hand. Past about 40 it stops reading as
one and becomes a paste. When the real text does not fit the bar available, **cut the text
rather than accelerate it**, and record the departure from the product in the script.

Give each character a cost rather than a constant step, a space and a full stop several times
a letter, and the typing has the rhythm of a hand instead of a scroll. Derive the costs from
the text, not from a random number, so every render types identically.

The caret belongs to this: solid while characters are arriving, blinking only when they stop.
A caret blinking through the typing says the field is idle.

## What is typed must land in the thread

A shot that shows a request being typed and sent, then something being built, needs the
request to appear as a message. Without it the answer has no visible cause: the viewer sees a
machine producing something nobody asked for.

## A growing panel passes behind its input bar

In a chat-like interface, content scrolls and the input bar stays at the bottom. A static
recreation does not scroll, so by the third block the content passes **behind** the bar and
disappears. Move the column up so the last item rests just above the bar, as the real product
does when it scrolls. The offset is calculated, not chosen:
`min(0, (top of bar - margin) - bottom of element)`.

And the container **fades** over its last pixels instead of cutting off: a line of text cut
sharply just above the bar reads exactly like text hidden behind it. A mask gradient of about
70px is enough, and that is what real interfaces do.

## The resting state of a control belongs in the markup

A placeholder written only by the shots that drive a field leaves the other shots showing an
empty box. It is invisible while a shot plays alone and obvious in the edit: the previous
shot ends with the placeholder on screen, the cut lands on a bar with nothing in it, and the
text appears to vanish. Put the idle text in the HTML so every shot inherits it, and let the
typing shots overwrite it. Same for a blinking caret, which belongs to a focused field.

A seam check catches this only if you read the number rather than the threshold: text is a
handful of pixels on a full frame, so the difference moved from 0,21 to 0,27, well under
anything that looks alarming.

## Remove what no longer helps

When the camera moves toward one part of the interface, elements with nothing more to say at
that moment **leave the frame** instead of staying in it. An unnecessary element holds the eye
and muddies the reading.

And do not play an animation during a decisive camera move. Bars growing while the camera
closes in makes both hard to read: the eye cannot tell what is moving. Finish the approach,
then start the animation while the camera only drifts.

## A video inside a shot

A `<video>` element does not advance deterministically in frame-by-frame rendering: its
playback follows the media clock, which rendering freezes. Separate images do not work
either, for a subtler reason: rendering freezes the clock before loading finishes, so the
first images display and the later ones never load. The video appears to start and then
freeze.

**Use an image sheet**: a single image holding every frame in a grid, loaded in one go during
the start delay, with one cell shown at a time by moving the background position.

```bash
ffmpeg -ss <start> -i <clip> -t <duration> \
  -vf "scale=<w>:<h>,fps=15,tile=<cols>x<rows>" -frames:v 1 -q:v 3 sheet.jpg
```

The sheet must cover **the whole time the element is on screen**: past its last cell the
image freezes, which is visible. Give the element the exact ratio of one cell, with
`aspect-ratio`, not a fixed height: the sheet is painted as a background that stretches to
fill and never crops, so any change to the element's width silently squashes what is in it.

## A stock person does not look like a real recording

A film that recreates a product can afford stock footage everywhere except in a player. Stock
is evenly lit and framed like an advertisement, and it reads as an advertisement. A real
recording looks nothing like that: a laptop camera pointing up, a plain wall behind, uneven
light, and a 4:3 frame the player letterboxes. That is what makes the shot read as evidence
rather than as illustration.

Two obligations follow. The consent that covers the original recording does not cover a
marketing film, so clear it before publication. And the image sheet stays **outside** any
repository, with the command that rebuilds it written in the production's script: a clone
carries whatever is committed to it, and this is a real person's face.

## People on screen

No real customer data. Conversations, figures and quotations are invented. Invent two or
three people and bring them back from one film to the next, so the product feels inhabited by
the same team: a film that invents new names each time feels like a mockup. Name the
logged-in user once and keep that name too.

## Full-frame titling

Four things happen per text fragment, in this order:

1. **The first word arrives very large and settles**, about 1,9x its final size, over half a
   second. It provides the impact; without this entrance the title falls flat.
2. **The rest of the fragment arrives next**, letter by letter, lifted by a wave moving left
   to right.
3. **The fragment holds** for about a second.
4. **It exits to the left** without changing size.

**Each fragment is scaled to occupy the same width**, around 60% of the frame in 16:9 and
0,76 in a square. A long fragment is therefore smaller than a short one: that gives the
scroll its regularity, and it is the least obvious thing about it. Fragments are two to four
words, 13 to 24 characters, never a whole sentence.

Letters that have not arrived take up no space, so the line recentres as it is written.
Otherwise the first word appears shifted left, at the position it will occupy in the final
sentence.

**A line must be fully written before it starts leaving.** Derive the hold from the text, not
from a constant: entrance, plus the per-word and per-letter delays of the longest fragment,
plus the time the last letter takes to arrive, plus a little air. The interval between two
fragments is at least the hold plus the whole exit. The exit curve is a cube, so a line
barely moves during its first half and stays fully opaque in the middle of the frame: a
fragment starting two tenths early prints itself over the one leaving, and both stay
perfectly legible.

**Say what the viewer gains before saying how it works.** An opening that asks people to
solve a riddle only lands for someone who already lives the problem. And a pronoun on a
full-frame card needs its antecedent on the same card.

**Do not announce what the demonstration will prove.** A card stating the promise just before
a demo that shows it doubles the length without adding anything. The symptom is simple: more
than ten seconds of text before the product appears, with identical grammar from one block to
the next.

## The end card

The mark is born as a point at the centre of the frame, grows to full size in about two
thirds of a second, holds still for just under a second, then the wordmark unfurls to its
right, revealed by a clip opening left to right with a strong ease-out over roughly a second.
The lockup then holds for the music tail.

The unfurl and the recentring are driven by the **same eased value**, so the wordmark
appearing and the block sliding left read as one gesture rather than two. Reference
animations of this kind usually come from an interface, where the icon is anchored left and
barely moves; a full-frame end card cannot borrow that anchoring, and the icon has to travel
from the centre of the frame to its place in the lockup.

Set the wordmark **below** the proportion of the drawn mark, which puts the letters at about
half the height of the sign, and centre the two on the same line. Matching their heights
makes the word shout over the sign.

Verify it on the rendered file, not on the page: extract every frame, measure the ink
bounding box, and read the mean difference between consecutive frames. A clean render shows
the box centred within a few pixels during the hold, a smooth rise and fall across the
unfurl, and exact zeros while the lockup is still.

## Sound

Synthesized effects, never downloaded samples. The scene declares its markers in a JSON
block and the build script makes the soundtrack from it, so the sound stays aligned when the
edit moves.

**Only sonify what really makes a sound.** Camera whooshes and small interface opening sounds
were tried and removed: a camera move has no sound in reality, and a synthetic interface
response right after a click does not sound like the response, it sounds like a click defect.
What is left is the click itself, a press and a release 55ms later, two dry transients.

**Absolute levels, no global mix normalization.** Normalization means that lowering one sound
raises all the others, so no setting stays predictable. Reference: a click around -8 dBFS.
Sound supports the image, it does not carry it: if you notice it, it is too loud.

## Cut the film to the track

Measure the tempo, the bar, and the two or three hard points of the piece: a re-entry after a
break, the start of a build, the last hit before it drops. Then place the film's own beats on
that grid: the opening on a hit, a click on a downbeat, the build entering on the gesture
that carries the argument, the logo born as the music falls away.

A piece is taken from the track **at a downbeat** and laid at a second of the film; two pieces
spliced on downbeats keep the pulse, so a body section and a build can meet with no audible
seam.

**Being on the pulse is not enough.** A verse followed by a build at full level reads as a
step, so bring the louder piece in at the level of the one it follows and let it climb over a
bar or two. The opposite trap is just as easy: a ramp starting at 0,45 of full came in four
decibels **under** the intro it followed, and the loudest section opened with a dip. Set the
entry level by measuring the sections in dBFS, not by ear, and check that the numbers climb.

Watch the overall level too: a bed whose peak sits near 0,3 sounds thin next to any other
video in a feed. Around 0,8 peak and -19 dBFS over the body is a reasonable target.

## Traps that cost a render

- **Never write `style.opacity *= ...`.** A property never written is the empty string, and
  multiplying it gives zero: the element disappears from the first frame, silently. In the
  same shot, an element whose opacity was already set survives while the other does not.
  Assign directly, or read with `parseFloat(...) || 0` first.
- **An entrance or exit added afterwards belongs inside the animation loop.** Placed after the
  function closes it never runs: the shot renders with no visible error, but the element
  appears abruptly.
- **A shot can render with no stylesheet at all.** If the scene is assembled from a template
  through string formatting, doubled braces meant for the formatter can survive into the
  output: the browser drops the invalid CSS in silence, the JavaScript keeps running, and the
  shot looks built and is unstyled. Checking that something is on screen does not catch it.
  Read the geometry back instead: print `getBoundingClientRect` for the elements that matter
  and dump the DOM at a frozen time. An element sitting at its intrinsic size in normal flow
  means the stylesheet never applied.
- **Beware the size a screenshot is actually taken at.** Headless Chrome does not give the
  same viewport to `--dump-dom` and to `--screenshot`, so a unit based on the viewport comes
  out several percent off in one of them. Ratios survive this, absolute pixels do not: read
  proportions from screenshots, and take any figure quoted in pixels from frames extracted
  from the rendered file.
- **A file rewritten at the same path can become unreadable in an editing tool.** Editors
  cache by path. A shot rendered ten times under the same name may stop displaying although
  the file is technically identical to the others. The answer is to change the filename, not
  to render again. For final deliveries, add a silent audio track and `+faststart`: some
  tools reject or misdisplay a video with no audio track.
