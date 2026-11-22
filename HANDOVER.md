# Handover: KODA × Cosh Living, best-of cut

Written 22 Nov 2026. The old session ("Video edit master teserract") has grown to 413 MB and freezes the app when opened, so don't go back to it. Start here.

## Read first
1. `docs/MASTER-DIRECTIVE-BEST-OF.md`: Aaron's full brief for this cut. It's the job.
2. `docs/rejected/`: four frames Aaron sent of rejected shots. Nothing like these goes in.
3. `README.md`: how the engine works (`film.js` is the edit, `render.mjs` renders, `audio/` holds the score and voice).
4. Memory notes `koda-at-cosh-living-film` and `koda-v23-hard-fail` (in the Desktop project's memory).

## Where it stands
- Git branches: `v1` (tag `v1.0`, the first draft, frozen), `v2`, `v2.3` (checked out). V2.3 was a **hard fail**: real material was swapped for composites and hand-drawn lamps.
- **V2.2 is the reference master**, not V2.3. Every version is now a source library.
- Source library reel: `rough/ASSEMBLY-koda-at-cosh-living-all-versions-1080p.mp4` (sections in `rough/ASSEMBLY-sections.txt`; copies in `~/Desktop/KODA at Cosh Living - rough cuts/`).
- **Uncommitted work in `film.js`** (about 70 lines):
  - `v=best` is the 90 s best-of cut: DEDON and Potocco stills from `src/best/`, Occhio Era films, Pablo's own Uma and Uma Mini photographs from `src/situ/pablo/`, A-N-D, Arkoslight, Lodes and Occhio films. No composites. Photos are held still, with no fake camera moves.
  - `cut=nb` is a 63.4 s B-roll set to "Nothing in Our Way" (Out To The World), from 2:15.1 to the end of the track, 93.25 bpm, bar = 2.5737 s.
  - An earlier render of the best-of is `rough/review-BEST-…-1080p.mp4` (made before the last label and Pablo-rhythm changes).

## Fix this first
`film.js` currently throws on load. `const NB` is declared at about line 158, but line 36 (`if (VBEST || NB)`) reads it first, which is a temporal-dead-zone error that stops **every** cut from rendering. Move the `NB` line up beside `VBEST` (about line 9). Also, the `WM` line lost its comment when `VBEST` was inserted; tidy that up.

## What was running when it stopped
The disk filled up (491 MB free). The job "prepare B-roll audio and render review frames for both cuts" failed. Aaron has since freed 30 GB.

Next steps, in order:
1. Fix the `NB` bug, render a contact sheet of both cuts (`v=best` and `cut=nb`), about one frame every 1.5 s.
2. Check every frame at **full size**: real manufacturer material only, nothing floating, nothing drawn, nothing pasted on, and the right thing in front.
3. Prepare the B-roll's music cut, then render final copies of both (1080p review, plus a phone copy under 30 MB).
4. Commit on a new branch `best` (keep `v1` and `v2.3` untouched), update `ASSET-REGISTER.md`, and send Aaron the files with section timecodes.

## Aaron's rules for this job
- Render everything without asking for approval until it's done (his words: "Render all do not ask for approval until completed").
- Lighting first, then that lighting in beautifully furnished designer rooms. Use the brands' own films and photographs: "You have amazing brand videos from each lighting and furniture brands."
- Never generate, draw, composite or superimpose a fixture. Keep what works; cut only what he names; cut by timecode when he gives one.
- Don't put brand labels on every shot under a dark band, and don't run eight Pablo photographs at one bar each, which reads as a slideshow.
- Confidential and local only: not on GitHub, not published.
- Delete only files you made, and only once he says yes.

## Keep the new session light
The old session froze because it took in 670 full-size images. Review frames as small contact sheets, open full-size crops only where needed, and don't read whole videos or large images into the chat.
