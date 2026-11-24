# Remix brief (Aaron, 24 Nov): :30, :45 and :60 pieces on four tracks, "super creative"

Tracks are copied into `audio/`: `music-hiyaku-sugoi.mp3`, `music-shy-millionaire.mp3`, `music-berliner-skyline.mp3`, `music-smiling-in-the-rain.mp3`.

## Track analysis (numpy onset grid; downbeats confirmed by per-beat loudness)

| Track | BPM | Bar 0 at | Beat | Bar | Structure |
|---|---|---|---|---|---|
| Shy Millionaire (Out Linear) | 112.99 | 0.465 s | 0.531 s | 2.124 s | intro 0–5; build 6–14; **drop bar 15**; full to 55; breakdown 56–63; return 64; natural ending 76–80 |
| Sugoi (Hiyaku) | 106.66 | 0.316 s | 0.563 s | 2.250 s | quiet bars 0–4; **first hit bar 5 (11.57 s)**; full from about bar 10 |
| Berliner Skyline (Wendy Marcini) | 72.67 | 0.499 s | 0.826 s | 3.303 s | steady groove bars 0–19; **lift bar 20 (66.6 s, downbeat confirmed)**; full to 43; fade 44–45 (about 150 s) |
| Smiling in the Rain (Wendy Marcini) | 80.00 | 0.094 s | 0.750 s | 3.000 s | soft intro 0–6; **lift bar 7 (21.1 s)**; **full drop bar 16 (48.1 s, confirmed)**; full to 64; outro 65–72; end about 219 s |

## Still to do

1. Generalise `tools/cut_phil.py` so each EDL picks its track (BPM, bar 0, gain) instead of the fixed Shy grid.
2. Add creative devices:
   - blackout beats (lights off, then the shot hits on the downbeat);
   - 2-frame ivory flash cuts;
   - kinetic type cards ("LET" / "THERE" / "BE" / "LIGHT" on four beats, then brand names);
   - pillar reveals (lanes switching on one by one).
3. Design and render the three pieces one at a time, then check, deliver, and copy to "For Google Drive":
   - **:30** on Smiling in the Rain: bars 13–16 riser into the drop at bar 16, ending in the outro;
   - **:45** on Berliner Skyline: slow, heavy, cuts on the beat or half-beat, with the lift at bar 20 as the hit;
   - **:60** medley: Sugoi's opening hit into Shy Millionaire's drop, joined on the bar.
