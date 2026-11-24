# Phil's hero lights: sourcing log

One entry per product as Aaron finds it (24 Nov 2026 onward). Files live in `src/phil/<brand>/<product>/` (not in git). Each entry records the source, the facts we may put on screen, and the frames picked for the montage.

**Montage rules:**
- Manufacturer films and photos only. Stills are held, with no fake moves.
- Portrait gallery images run as **diptychs**: two portraits side by side on graphite with a thin gutter. That keeps them full-frame, with no crop that loses the pendant or the table.
- Captions: brand in small tracked capitals, product name under it.

## Status (24 Nov)

| # | Memo said | Product | KODA stills | Film | Montage block |
|---|---|---|---|---|---|
| 1 | Axia | Lodes Axia | ✅ 10 + 6 Lodes press | ✅ Lodes film + Milan showroom (captures) | ✅ built, 5 bars |
| 2 | Stitch | Lodes Stitch | ✅ 44 (3 scenes, 4 details) | ✅ Lodes night-garden film (capture) | ✅ built, 4 bars |
| 3 | Random | Lodes Random (Cloud, Cluster, Solo) | ✅ 48 | ✅ four Lodes films (captures) | ✅ in the Lodes pillar block |
| 4 | Column 300 / 175 horizontal | A-N-D Column 300 and 175 Horizontal, Amber | ✅ 31 KODA + 27 A-N-D project photos | ✅ Column film (capture) + A-N-D homepage film (1080p) | ✅ built, 5 bars |
| 5 | Ivy | Brokis Ivy Horizontal | ✅ 14 KODA + 16 Brokis image bank (up to 8688 px) | none found (Brokis site has no film) | ✅ built, 4 bars (stills) |
| 6 | "Celia" | David Pompa Cilia Pendant 60 and 60 Double | fetching | to find | — |
| 7 | Tempo | a-emotional Tempo Andante and Vivace ("chaser" unclear) | fetching | to find | — |
| 8 | "Pantea" | Pablo Pantaya | fetching | ✅ Pablo's film, 1080p (`src/video/koda-home-7.mp4`) | ✅ built, 3 bars |
| 9 | Totem | Pablo Totem Pendant Up/Down | fetching | to find | — |
| 10 | "Sharlitz" | MUG Charlotte Single pendant (by sound; **confirm**) | fetching | to find | — |
| 11 | "Maury" | RBW Mori Pendant (by sound; **confirm**) | fetching | to find | — |
| 12 | a-emotional Clouds | not in KODA's catalogue | — | **Phil's video** | — |
| + | (Aaron's addition) | a-emotional light Nevo | — | ✅ a-emotional film (capture) | ✅ built, 3 bars |

---

---

## 1. Lodes Axia

| | |
|---|---|
| KODA page | https://kodalighting.com/products/25121 (Aaron, 24 Nov) |
| Type | Pendant, a contemporary chandelier: a central axis feeds the branching arms, so the light flows within the structure rather than along a cable |
| Designers | Vittorio Venezia and Carolina Martinelli |
| Size | Ø 78 × 87 cm; canopy Ø 15 × 5 cm |
| Finishes | Glossy Bronze, Black Chrome |
| Light | 2700 K or 3000 K |
| Materials | Stainless steel, PVD coating, glass diffusers |
| Phil's note | "Flat-pack, easy to install." This isn't stated on KODA's page; **confirm with Phil** before it goes on screen. |

**Files**
- `src/phil/lodes/axia/axia-01…10.png`: KODA's gallery (10 images). 01–04 are rooms (portrait, 1800 × 2400), 05 is the lobby (landscape, 2560 × 1707), 06–08 are close-ups, and 09–10 are cut-outs (not for use).
- `src/phil/lodes/axia/lodes-press/axia-rgb-{1,2,5,6,7,8}`: Aaron's six Lodes press files (AVIF, plus JPEG copies). They're the same images as KODA 01, 03, 07, 08, 06 and 02, at the same 1800 × 2400.

**Montage picks**
1. **Lobby at night** (`axia-05.png`, landscape): three Axias lit warm over bouclé seating and a bronze desk. The one full-frame 16:9 shot, and the lead.
2. **Diptych:** arched dining room with the marble table (`axia-02` / `axia-rgb-8`), next to the bronze glass close-up (`axia-06` / `axia-rgb-7`).
3. **Diptych (optional):** double-height lounge (`axia-04`), next to the three-globe detail (`axia-08` / `axia-rgb-6`).

**Film:** `src/phil/lodes/axia/axia-screen-capture-portrait.mov`, Aaron's screen capture of the Lodes Axia film (portrait, 774 × 1230, about 60 fps, 25.3 s).
- The film is one continuous move of about 11 s, from the whole chandelier in the room into a close-up of a glass diffuser. The capture plays it twice; the loop restarts at 11.27 s.
- Use one clean pass, **0.0–11.2 s**, cropping the thin grey strip along the top edge.
- At 1080p it runs as a full-height portrait panel (about 680 × 1080, a slight downscale), either paired with a still as a diptych or centred on graphite.

**For the final cut:** ask Lodes or Phil for the original film file. A screen capture is fine for review, but the original will be sharper and free of capture artefacts.

**Milan showroom film:** `src/phil/lodes/axia/axia-milan-showroom-capture.mov`, Aaron's capture of Lodes' 45 s social film from the Milan showroom (portrait, 704 × 944; the capture runs slightly past one loop). It has the designers talking and visitors in the showroom. **Per Aaron, use only the moving shots of the light:** 12 light-only selects, 0.4–1.3 s each (about 9 s in all), listed with in and out points in `docs/phil/axia-milan-selects.json`. At 1080 it is enlarged 1.14×, so ask Lodes for the original for the final.

**Montage plan for Axia:** the film panel next to the lobby or arched-dining still, then the lobby full-frame.

---

## 2. Lodes Stitch (outdoor)

| | |
|---|---|
| KODA page | https://kodalighting.com/products/807 (Aaron, 24 Nov) |
| Type | A family of outdoor lanterns (pendant, wall, table/floor) in a technical outdoor fabric ribbon woven through a metal cage. Lodes: "the light emotions associated with a beach at sunset". |
| Finishes | Four: black, sand, terracotta red and green (36 variants on KODA) |
| Phil's note | Outdoor and Mediterranean, "looks like one of their ads". It's the **rooftop lead** into the montage. |

**Files:** `src/phil/lodes/stitch/stitch-01…44`, KODA's gallery.
- **01** is the dusk sea terrace with pool, loungers and bar pendants (landscape, 1800 × 1200).
- **02** is the garden outdoor kitchen (landscape).
- **03** is the sea-view restaurant with Stitch pendants (landscape).
- **04** is the wall lantern, lit; **05** the pendant pair, lit; **06** the terracotta weave close-up; **07** the black cap close-up (all portrait).
- **08** is a portrait crop of 01.
- **09–44** are cut-outs (not for use).

**Montage block (4 bars):** 01 full-frame under the caption (2 bars), then a diptych of 05 and 06 (1 bar), then 03 full-frame (1 bar). 02 is spare.

**Still needed:** a Lodes Stitch film, if one exists. The landscape stills are 1800 px wide, so at 1080p they're enlarged 1.07×, which is fine.

**Stitch films** (Aaron's screen captures, 24 Nov):
- `stitch-film-capture.mov` is the Lodes night-garden film: portrait, 764 × 1026 (3:4, the panel shape), 29.8 s, looping at about 16 s, with a LODES end card. Use the **first pass only**, because the second pass caught the macOS "Stop Screen Recording" button. The shots:
  - 0–3.5 s: lanterns among the foliage
  - 3.6–7.6 s: pergola lounge, with a floor lantern in front of the dining pendants
  - 7.7–10.8 s: floor lantern by the bench
  - 12.2–16.0 s: dining table under three Stitch pendants
- `stitch-film-capture-wide.mov` has the same shots in a taller portrait (764 × 1262, about 9:16), ending on a **"vastu"** end card (12.2–14.5 s; probably a stockist's cut). Keep it as a framing alternative, since it shows more of the pergola beams overhead.

**Montage block (4 bars, caption lower right):**
1. Terrace still 01, full-frame (6 beats).
2. Diptych, both panels from the film: pergola lounge | dining under three pendants (6 beats). They read as one continuous pergola.
3. Diptych: floor lantern film | the pendant pair, still 05 (4 beats).

---

## 8. Pablo Pantaya

| | |
|---|---|
| KODA page | https://kodalighting.com/products/pntypndt |
| Designer | Patricia Urquiola (from the film's credit card; Pablo, with Haworth) |
| Film | `src/video/koda-home-7.mp4`: Pablo's Pantaya film from KODA's homepage (Vimeo 1245314168), 1920 × 1080, 67 s. Already used in the earlier cuts. |

**Montage block (3 bars, all full-frame, light-only shots):**
- dining room with the long table, from 14.6 s (4 beats)
- the trio glowing, from 28.75 s (4 beats)
- green Pantaya over the artwork, from 41.95 s (2 beats)
- blue Pantaya in the dark, from 51.35 s (2 beats)

The designer interview (about 6 s) and the shots with hands (12 s and 39 s) are excluded.

---

## 3. Lodes Random (Cloud, Cluster, Solo)

**KODA pages:** /products/ran_cl_8 (Random Cloud, 23 lights, Ø28) and /products/ran_so_5 (Random Solo cluster).

**Stills:** `src/phil/lodes/random/random-01…48`, KODA's gallery.
- Portrait: **01** copper Cloud, **03** living room, **04** chrome cluster in a corner.
- Landscape: **02** dining, **06** retail, **24** reception-wall installation, **27** a long hall.

**Films** (Aaron's captures, 24 Nov):
- `random-cloud-film-capture.mov` (portrait, 764 × 1262): one 13.7 s shot. Tree shadows cross a plaster wall and fade to dusk, then the glass cluster glows warm; a day-to-night in miniature that rhymes with the establishing shot. Use 4.9–13.5 s. LODES card from 13.75 s.
- `random-cloud-capture-2.mov` (portrait, 778 × 1268): a chrome cluster glowing in a dark room with the camera moving (6.3–10.95 s), then spheres in close-up (11.05–12.3 s). There's a LODES card from 1.5 to 6.2 s.
- `random-cloud-youtube-capture.mov` (2812 × 1396, from YouTube): the Random Cloud **hallways** film; Aaron: "the scenes in the hallways transitioning are impressive". YouTube's pause icon sits under the cluster from about 1.5 to 5.7 s, and a replay icon covers the frozen end frame.
  - **Cleaned:** `random-cloud-hallways-clean.mp4` takes 5.75–10.68 s (stone arches, cutting to the tree-lined hallway). It needs no masking because it starts after the icon is gone. Cropped to 16:9 and scaled to 1920 × 1080, a downscale.
  - **Masked:** `random-cloud-stairs-masked.mp4` is the stair shot (1.95–5.10 s) with the icon removed by delogo. A faint smear remains under the spheres, so it's not for the final; **ask Lodes for the original film**.
- `random-solo-capture.mov` (portrait, 704 × 960): copper Random Solo pendants over a kitchen island (10.45–14.45 s), a dining table (14.55–15.4 s), and pendant close-ups (20.15–24.9 s). LODES cards run from about 4 to 10.3 s.

---

## 4. A-N-D Column (300 and 175 Horizontal, Amber)

**KODA pages:** /products/col-300_3 (Column 300 Horizontal, Amber) and /products/col-175 (Column 175 Horizontal, Carbon).

**Stills:** `src/phil/a-n-d/column/column-01…31`, 17 of them landscape. **24** is 4800 × 3200 and **21** is 2800 × 1867.

**Film:** `column-film-capture.mov`, Aaron's capture of A-N-D's Column film (portrait, 768 × 1286, 26.8 s, looping at about 15 s). Each shot runs about 2 s:
- 0–1.3 s: vertical Column in a curtained lounge
- 5.43–7.13 s: horizontal Column over a kitchen island
- **7.13–9.17 s: amber horizontal Column over a dining table** (Phil's shot)
- 9.17–11.2 s: bathroom, ceiling and floor Columns
- 11.2–13.13 s: table Column by a window
- From 15.13 s the loop repeats; the kitchen is at 21.3 s and the amber dining table at 23.0 s.

Skip the "Column / A-N-D" title cards (1.3–3.5 and 16.8–19.4 s) and the white-background product animations (3.5–5.4, 13.1–15.1 and 19.4–21.3 s).

**Aaron's reference shot:** the amber horizontal Column over a long dining table, with wishbone chairs and white tulips. It's **KODA still 20** (`column-20.png`, 2493 × 4432). The block opens on it full-frame, cropped 16:9 with the Column near the top and the table and chairs below. The film has the same room moving (7.13–9.17 s), and that opens the pillars.

**A-N-D homepage film** (`src/video/koda-home-5.mp4`, 1080p; Aaron's `file.mp4 (1080p)-2.mp4` is the same file). The horizontal Column appears in three shots, found fresh on 24 Nov and listed in `docs/phil/and-film-selects.json`:
- **wide** (10.24–11.68 s): showroom, a long horizontal Column of about ten segments, with an amber vertical Column through it
- **macro** (8.64–10.16 s): along the tube's glass ribs
- **close** (5.52–6.20 s): clear ribbed segments on their cables

**A-N-D's own project photos** (`src/phil/a-n-d/column/and-site/`, 27 files from a-n-d.com/COLUMN-PENDANT at original size; credits in the filenames). They include COS Seoul (Studio Brinth), Din Tai Fung by Rockwell Group (Jason Varney), Massara by Sarah Carpenter Studio (Brian Ferry), Dorsia by Ivy Studio (Alex Lesage), Burgers Residence, NORR11 × A-N-D, OAKV by Atelier Carle, TEC by MRDK, Above90's Lock-Mortice, Studio Ines Deschodt and Saint-Cloud by Atelier Ha.

**A-N-D's dim-to-warm film** (Vimeo 1119263784, portrait, on the Column page) is restricted to embedding on A-N-D's site, so it couldn't be downloaded. **Aaron: screen-capture it from the page** if you want it; it shows the dim-to-warm amber Phil described.

**Montage block (5 bars):** still 20 (4 beats, caption) → film wide (2 beats) → pillars (12 beats: the film's amber dining, bathroom, kitchen and table lamp | KODA still 21, amber dining, lounge, kitchen | COS Seoul, lounge, Massara, bathroom) → film macro (1 beat) → film close (1 beat).

---

## 5. Brokis Ivy Horizontal

**KODA pages:** /products/pc1070 (Horizontal 8) and /products/pc1069 (Horizontal 7; 5 of its 7 images match pc1070). Aaron, 24 Nov.

**Brokis image bank** (`src/phil/brokis/ivy/brokis-site/`): 16 photos from Brokis' collection index (brokis.b-cdn.net/imagebank/collections/PF203), full-resolution JPEGs of 6000–8688 px, credited Martin Chum (one by Suprema). Aaron's reference is **PH1466**, Ivy on dark grey.

**Key frames:**
- PH8265 (Suprema): a lounge with many Ivys over the sofas (open space)
- PH1397: over a dining table
- PH1396: portrait, over a dining table
- PH7568: garden pavilion
- PH7569: stone-and-glass garden room
- PH1463: lit on black

**Film:** none on Brokis' page or in the image bank. Ivy runs on held stills.

**Montage block (4 bars, full-frame):** Suprema lounge (4 beats, caption) → PH1466 dark grey (2) → PH1397 over the table (2) → PH7568 pavilion (2) → PH7569 garden room (2) → diptych of PH1396 dining and PH1328 shade close-up (4).

---

## 6. David Pompa Cilia (Pendant 60, 60 Double)

**Film:** `src/phil/david-pompa/cilia/cilia-film-capture.mov`, Aaron's capture of David Pompa's Cilia explainer (portrait, 768 × 1286, 40 s, looping at about 32 s). Most of it shows hands demonstrating the fitting, some with **burned-in subtitles**; those parts are excluded. Light-only selects:
- 23.6–24.5 s: upper disc glowing, lower disc dark
- 26.0–27.05 s: both discs glowing (after the hand leaves frame)
- 27.15–28.85 s: warm close-up of the disc edges and connector

**Stills:** `cilia-01…13`, KODA's gallery. **02** is landscape at 6000 × 3678.

---

## a-emotional light Nevo (Aaron, 24 Nov)

**Film:** `src/phil/a-emotional/nevo/nevo-film-capture.mov`, Aaron's capture of a-emotional's Nevo film (portrait, 768 × 1286, 60 s). It has a woman presenting, a hand touching and turning the light, a "NEVO" title card, and **subtitles burned in** near the bottom (y ≈ 1054) on most shots.

**Aaron's brief:** "use the light turning and close up images of the texture. The light is the hero, do not use the woman presenting nor any of the text."

**How the block meets it:**
- Pillars crop to rows 4–1004, so the subtitle band is never in frame.
- Shots with the presenter, a hand or the title card are excluded. The turning shot is used only from 30.75 s, after the hand leaves, and the room shot only from 18.0 s, after a reaching hand leaves.
- Every pillar frame of the built block was checked.

**Light-only selects** (s):
- Texture: 1.1–3.05, 3.25–5.95, 37.95–40.85, 54.55–56.3, 56.5–58.4
- Spiral: 26.2–28.8
- Turning: 30.75–31.65, 35.45–36.3
- Underside, lit: 19.3–22.5, 52.7–54.35
- Nevo in the room: 18.05–19.1, 36.45–37.8, 41.05–42.4

**Montage block (3 bars, pillars):** textures | room, turning, profile turn, with the art, underside, room | underside, spiral, texture.

**Confirmed (Aaron, 24 Nov):** Nevo is a **separate piece** from Phil's "Clouds". It's an addition Aaron chose for the a-emotional light section. Clouds still needs Phil's video.

**Pantaya addition (Aaron, 24 Nov):** `src/phil/pablo/pantaya-icff-capture.mov`, Pablo's portrait ICFF 2026 promo (768 × 1286, 34.6 s), captured by Aaron. "PANTAYA" is lettered along the bottom of every shot, so the pillars crop to rows 4–1154; the Pablo and ICFF/Javits title cards are excluded. It adds the **wall-mounted oval Pantaya**. The block now ends on a 1-bar pillar: the oval from 16.3 s (clear of the Javits card's dissolve) | green mesh close-up from 2.25 s, then 28.2 s | green pendant over the artwork from 20.3 s (clear of the dissolve).
