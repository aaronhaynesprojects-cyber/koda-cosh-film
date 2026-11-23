"""Download KODA (kodalighting.com, Shopify) product galleries into src/phil/<brand>/<product>/ and print a summary.
  python3 tools/fetch_koda.py"""
import json, os, subprocess, urllib.request
ITEMS = [("lodes", "random", ["ran_cl_8", "ran_so_5"]), ("a-n-d", "column", ["col-300_3", "col-175"]), ("brokis", "ivy", ["pc1070"]),
         ("david-pompa", "cilia", ["pa202-60", "pa202-60-p2"]), ("a-emotional", "tempo", ["tean04_ld", "tevi04_ld"]),
         ("pablo", "pantaya", ["pntypndt"]), ("pablo", "totem", ["tote-updwn"]), ("mug", "charlotte", ["charlotte-single-pendant"]), ("rbw", "mori", ["mp"])]
UA = {"User-Agent": "Mozilla/5.0"}
for brand, prod, handles in ITEMS:
    d = f"src/phil/{brand}/{prod}"; os.makedirs(d, exist_ok=True); seen, n, land = set(), 0, []
    for h in handles:
        p = json.load(urllib.request.urlopen(urllib.request.Request(f"https://kodalighting.com/products/{h}.json", headers=UA)))["product"]
        for im in p["images"]:
            src = im["src"].split("?")[0]
            if src in seen: continue
            seen.add(src); n += 1; ext = os.path.splitext(src)[1] or ".jpg"; out = f"{d}/{prod}-{n:02d}{ext}"
            if not os.path.exists(out): subprocess.run(["curl", "-sfL", "-A", "Mozilla/5.0", src, "-o", out], check=True)
            if im["width"] > im["height"]: land.append(f"{n:02d} {im['width']}x{im['height']}")
        print(f"{brand}/{prod} <- {h}: {p['title']}", flush=True)
    print(f"  {n} images; landscape: {', '.join(land) or 'none'}", flush=True)
