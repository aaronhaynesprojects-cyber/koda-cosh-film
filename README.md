# KODA at Cosh Living: 90-second concept film

Confidential. Local only: not on GitHub, not published.

- `film.js` is the whole edit: the shot list (`SHOTS`), titles, brand labels, the three concept composites (`buildConcepts`) and the end card.
- `audio/score.py` writes the score to `audio/score.wav`.
- `render.mjs` draws every frame in headless Chrome and pipes it to ffmpeg.
- `src/` holds the downloaded sources; `fr/` the 25 fps frames cut from the manufacturers' films.
- `ASSET-REGISTER.md` lists every source and its permission status.

```
~/Developer/.asr-venv/bin/python audio/score.py
node render.mjs sheet check 5,20,40,60,80 5                         # contact sheet → out/check.jpg
S=2 CRF=14 node render.mjs encode film/master-4k.mp4 audio/score.wav   # 3840×2160, 25 fps
REVIEW=1 CRF=18 node render.mjs encode film/review-1080p.mp4 audio/score.wav
```
