# KODA × Cosh Living reel: revision plan for Phil's brief

*Draft plan, 23 November 2026, for Aaron's approval. Nothing has been edited yet.*

## 1. What exists now

**The reel Phil reviewed.** "Built only from the brand videos on KODA's homepage" describes the **V1 film and the KODA brands B-roll**, branch `v1`, tag `v1.0`, in `~/Developer/koda-cosh-film`. Both are cut from the seven films on kodalighting.com's homepage (`src/video/`): Occhio Luna, KODA Lightspace, A-N-D, Pablo Pantaya and Arkoslight, plus a Lodes outdoor film that was downloaded but not used.

**The engine.** `film.js` draws every frame as a function of time; `render.mjs` renders it through headless Chrome and ffmpeg at 1920 × 1080, 25 fps. Cuts are selected by URL switch: `v=best`, `best3` and `best4` are Aaron's best-of cuts, and `cut=broll` is the B-roll. Review copies get the First Creek Studios run-in and the 3-2-1 countdown (`~/Developer/first-creek-brand/firstcreek.py`).

**Approved style that carries over:**
- Manufacturer footage and photos only, with nothing composited, drawn or generated.
- Restrained captions: the brand name in small tracked capitals at lower left.
- The Rocket Jr score (112 bpm, cuts on the bar), with or without Marie's narration.
- The KODA × Cosh Living end card.

### Assets already on disk, by product in the brief

| Brief item | On disk | Status |
|---|---|---|
| Lodes **Stitch** | none (catalogue entry with 44 product images on kodalighting.com) | Confirmed Lodes. Needs in-situ / outdoor imagery. |
| Lodes **Random** | Random cluster, Cloud and Solo stills (used in V1) | Confirmed. Room shots on hand. |
| Lodes **Axia** | catalogue entry only (10 images) | Confirmed: **Axia**, Lodes. Needs in-situ imagery. |
| a-emotional light **Clouds** installation | none | Brand isn't in the KODA data on disk. **Phil has the video.** |
| a-emotional light **Tempo** ("chaser") | none | (confirm) |
| A-N-D **Column 175 / 300 Horizontal**, amber | A-N-D homepage film (ribbed-glass columns); catalogue lists Column 175 Horizontal, Column 300 Vertical, and an Amber finish | Confirmed A-N-D. **Column 300 Horizontal** still to confirm. Needs an over-table shot in amber. |
| Brokis **Ivy** horizontal | none | The only Ivy in the data is **Lodes Ivy**. **(confirm the brand)** |
| David Pompa **Celia Pendant 60** | none | Brand isn't in the data. (confirm name and spelling) |
| "Sharlitz" pendant | none | Not found. (confirm brand and name) |
| Pablo **"Pantea"** | Pablo Pantaya film (`fr/p_dine`) | Almost certainly **Pantaya**. (confirm) |
| Pablo **Totem** pendant up/down | catalogue entry (23 images) | Confirmed: **Totem Pendant Up/Down**, Pablo. |
| "Maury" pendants (optional) | none | (confirm) |
| Occhio, Arkoslight (carousel) | Occhio Era films (4K), Luna and Mito stills; Arkoslight films and stills | On hand |
| Brand logos | KODA, Cosh, Occhio, Lodes, Arkoslight, A-N-D, Pablo | **Missing:** Brokis, a-emotional light, David Pompa, and any other brands KODA carries |

**Cosh Living** is the correct name (coshliving.com.au; it's already on the end card). "Kosh Living" is only a transcription.

## 2. Proposed reel: about 2:00 (length approved by Aaron, 23 Nov)

| # | Section | Time | Content |
|---|---|---|---|
| 0 | Open | 0:00–0:04 | Dark to light: one held manufacturer shot with a slow light-up (an Occhio Era switch-on or the a-emotional Clouds). |
| 1 | Brand carousel | 0:04–0:34 | Each KODA brand for about one bar (2.1 s): its signature shot with its logo. It ends on a **logo wall**, every brand on one card, held for about 3 s. |
| 2a | Breadth | 0:34–0:50 | Fast cuts, one beat (0.54 s) per product, through every hero product in the order below. |
| 2b | Depth | 0:50–1:42 | A longer beat (4–8 s) on each product in a real setting. Outdoor and Cosh-relevant pieces lead. |
| 3 | Together | 1:42–1:57 | KODA lighting in Cosh's own spaces (showroom, rooftop). See section 4. |
| 4 | End card | 1:57–2:02 | KODA × Cosh Living. |

### Section 2b order and beats (about 52 s)

1. **Lodes Stitch**: outdoor, Mediterranean, "looks like one of their ads". About 7 s; the rooftop lead-in.
2. **a-emotional light Clouds**: outdoor install plus the spray-on ceiling footage. About 8 s.
3. **Lodes Random**: about 5 s.
4. **Lodes Axia**: flat-pack, easy to install. About 4 s.
5. **A-N-D Column Horizontal** in amber, over a table, dimming down to warm. About 6 s.
6. **Brokis Ivy** horizontal, over a table or in an open space. About 6 s.
7. **David Pompa Celia 60**, single and double over a table. About 5 s.
8. **"Sharlitz"** pendant: about 4 s.
9. **Pablo Pantaya**: about 4 s.
10. **Pablo Totem** up/down clusters: about 4 s.
11. *(Optional)* a-emotional Tempo and the "Maury" pendants, if there's room.

The captions are as now: brand in small capitals, product name under it, held about 3 s. There's no pricing or commercial text.

### Section 3: what "together" can honestly show

KODA lighting in Cosh's showrooms and rooftop has never been photographed. The rules on this project (no composites, no generated fixtures) rule out faking it. Options for Aaron to choose from:
- **a. Editorial pairing (recommended).** Cut between a Cosh space (a showroom, a rooftop or a DEDON/Potocco setting) and the KODA piece that would sit there, as two halves of one idea. Use simple on-screen lines, for example "Rooftop · Lodes Stitch", then "Showroom · A-N-D Column". End on the KODA × Cosh Living card.
- **b. Labelled concept frames.** Placeholder cards such as `[CONCEPT: Lodes Stitch over the Cosh rooftop table]` until real photography exists, for example a test install at a Cosh showroom.
- **c.** Both: (a) in the reel, and (b) as stills in Aaron's separate pitch deck.

### Music and voice

- **Music:** Rocket Jr is approved but cut for 90 s. For about 2:00 it needs a longer edit or a second track. Options: extend Rocket Jr on its bars, the way earlier versions were edited, or use Maltese Midnights (84 bpm, 2:45), which is more relaxed and premium.
- **Voice:** none by default. Phil asked for breadth, depth and a close, and the tone is "not pushy". Marie's existing lines could cover the close only ("KODA at Cosh Living. Imagine what's possible.").

## 3. Placeholder policy

Any missing asset becomes a dark card in the house type, sized and timed like the real shot, for example `[ASSET NEEDED: Brokis Ivy horizontal, over table]`. That keeps the cut and the music locked while assets arrive, and the cards are swapped one by one.

## 4. Open questions

**Source of the names.** Phil's brief comes from a voice memo transcribed by Whisper, so every product and brand name is a phonetic guess. "Kosh" was already wrong for Cosh, and "Pantea" is almost certainly Pantaya. Treat "Sharlitz", "Maury", "Celia", "Tempo" and "chaser" the same way: match them by sound against KODA's catalogue, not by spelling.

If the original memo audio is available, the quickest fix is to re-transcribe it locally with Whisper's larger model, primed with KODA's brand and product names. That usually resolves names like these outright, and the timestamps let Aaron replay just the doubtful words.

**To confirm on kodalighting.com or with Phil:**
1. The brand of **Ivy** horizontal: Brokis, or the Lodes Ivy KODA lists?
2. Does **Column 300 Horizontal** exist, or is it Column 175 Horizontal / Column 300 Vertical?
3. **Celia Pendant 60**: does KODA carry David Pompa, and how is the name spelled?
4. **"Sharlitz"**: brand and product name.
5. **"Maury"** pendants: brand and product name.
6. a-emotional light **Tempo** and its "chaser" version.
7. Is **"Pantea"** the Pablo **Pantaya**?
8. The full list of KODA brands, for the carousel and the logo wall.

**Aaron's decisions (23 Nov):**
- Length about 2:00: approved.
- Music: Rocket Jr as a placeholder; Aaron will supply the final track. The cut is laid out in bars so it re-times to the new track.
- Section 3: to be decided 24 Nov.
- Big Ass Fans: out ("keep it design savvy"). The carousel is 12 lighting brands.

## 5. Assets to request from Phil / KODA

- The a-emotional Clouds video and the spray-on ceiling footage.
- Vector logos for every KODA brand.
- In-situ or lifestyle imagery or video for Stitch, Axia, Column Horizontal (amber, over a table), Ivy, Celia 60 (single and double), "Sharlitz", Totem clusters, Tempo and "Maury".
- Any photography of KODA product in a Cosh showroom, or permission to shoot a test install.
- Cosh rooftop and showroom photography for section 3, with Cosh's permission.

## 6. Build steps once assets are in

1. Aaron's website deep dive: download each brand's films and images into `src/phil/<brand>/<product>/`, and log each source in `ASSET-REGISTER.md`.
2. Add a new switch, `v=phil`, to `film.js`. Existing cuts are untouched, and the branch is `phil` off `best`.
3. Lay out the timeline on the bars, with placeholder cards where assets are missing. Send a contact-sheet preview.
4. Replace the placeholders as assets arrive. Use warm amber lighting states where there's a choice.
5. **QC:** watch the full render. Check frames at full size, audio sync and levels, and caption overflow.
6. **Deliver:** a 1080p review copy with the First Creek run-in and countdown, a phone copy, the shot list with timecodes, and the list of open placeholders and confirms.

**Out of scope for the video:** margin, addressable market, store numbers and exclusivity. Those go in Aaron's separate pitch.
