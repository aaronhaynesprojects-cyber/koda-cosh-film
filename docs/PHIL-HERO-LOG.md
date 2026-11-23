# Phil's hero lights: sourcing log

One entry per product as Aaron finds it (24 Nov 2026 onward). Files live in `src/phil/<brand>/<product>/` (not in git). Each entry records the source, the facts we may put on screen, and the frames picked for the montage.

**Montage rules:**
- Manufacturer films and photos only. Stills are held, with no fake moves.
- Portrait gallery images run as **diptychs**: two portraits side by side on graphite with a thin gutter. That keeps them full-frame, with no crop that loses the pendant or the table.
- Captions: brand in small tracked capitals, product name under it.

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
