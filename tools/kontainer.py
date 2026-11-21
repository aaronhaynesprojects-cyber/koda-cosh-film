"""Catalogue a Kontainer press library that the manufacturer shares by public direct link.
The direct link (published on the brand's own press page) gives a guest 'PRESS' session; this walks the
folder tree with it, writes catalogue.json, and fetches the small preview of chosen files.
Usage: python tools/kontainer.py catalogue <host> <direct-token> <root-folder-id> <outdir>
       python tools/kontainer.py previews  <outdir> [regex-on-path]
       python tools/kontainer.py original  <outdir> <file-id> ...      (full-resolution download, where permitted)"""
import sys, json, re, time, os, urllib.parse, http.cookiejar, urllib.request
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def session(host, token, folder):
    cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA)]; op.open(f"https://{host}/direct/{token}/folder/{folder}", timeout=40).read()
    x = urllib.parse.unquote(next(c.value for c in cj if c.name == "XSRF-TOKEN"))
    op.addheaders = [("User-Agent", UA), ("Accept", "application/json"), ("X-Requested-With", "XMLHttpRequest"), ("X-XSRF-TOKEN", x)]
    return op
def get(op, host, path, tries=3):
    for k in range(tries):
        try: return json.loads(op.open(f"https://{host}{path}", timeout=60).read())
        except Exception as e:
            if k == tries - 1: raise
            time.sleep(2)
def items(op, host, fid):
    out = {"folders": [], "files": []}
    for p in range(1, 60):
        r = get(op, host, f"/api/folders/{fid}/items/100?page={p}&orderFilesBy=name&orderFilesDir=asc&orderFoldersBy=name&orderFoldersDir=asc")
        out["folders"] += r["data"].get("folders") or []; out["files"] += r["data"].get("files") or []
        if p >= (r.get("pagination") or {}).get("last_page", 1): break
    return out
if __name__ == "__main__" and sys.argv[1] == "catalogue":
    host, token, root, outdir = sys.argv[2:6]; op = session(host, token, root); cat = {"host": host, "root": int(root), "direct_link": f"https://{host}/direct/{token}/folder/{root}", "retrieved": time.strftime("%Y-%m-%d"), "folders": [], "files": []}
    def walk(fid, path):
        r = items(op, host, fid)
        for f in r["files"]:
            im = f.get("images") or {}; vd = f.get("videos") or {}
            cat["files"].append({"id": f["id"], "path": path, "name": f["name"], "type": f.get("filetype"), "ext": f.get("ext"), "width": f.get("width"), "height": f.get("height"),
                "bytes": f.get("size"), "permission": f.get("permissions"), "created": f.get("created"), "description": f.get("description"),
                "thumb": (im.get("thumbnail") or {}).get("src"), "preview": (im.get("fullscreen") or {}).get("src"), "preview_w": (im.get("fullscreen") or {}).get("width"),
                "videos": {k: {kk: vv for kk, vv in (v or {}).items() if kk in ("src", "width", "height", "duration", "size")} for k, v in vd.items()} if isinstance(vd, dict) else {}})
        for d in r["folders"]:
            cat["folders"].append({"id": d["id"], "path": path + "/" + d["name"], "files": d.get("filesCount"), "bytes": d.get("filesSize")}); walk(d["id"], path + "/" + d["name"])
    walk(int(root), ""); json.dump(cat, open(f"{outdir}/catalogue.json", "w"), indent=1)
    print(len(cat["folders"]), "folders,", len(cat["files"]), "files; types:", {t: sum(1 for f in cat["files"] if f["type"] == t) for t in {f["type"] for f in cat["files"]}})
elif __name__ == "__main__" and sys.argv[1] == "previews":
    outdir = sys.argv[2]; rx = re.compile(sys.argv[3] if len(sys.argv) > 3 else "."); cat = json.load(open(f"{outdir}/catalogue.json"))
    tok = re.search(r"/direct/([^/]+)/", cat["direct_link"]).group(1); op = session(cat["host"], tok, cat["root"]); n = 0
    for f in cat["files"]:
        if not f.get("preview") or not rx.search(f["path"] + "/" + f["name"]): continue
        p = f"{outdir}/previews/{f['id']}.jpg"
        if os.path.exists(p): continue
        for k in range(3):
            try: open(p, "wb").write(op.open(f"https://{cat['host']}{f['preview']}", timeout=60).read()); n += 1; break
            except Exception: time.sleep(2)
    print(n, "previews fetched")
elif __name__ == "__main__" and sys.argv[1] == "original":
    outdir = sys.argv[2]; ids = [int(x) for x in sys.argv[3:]]; cat = json.load(open(f"{outdir}/catalogue.json")); byid = {f["id"]: f for f in cat["files"]}
    tok = re.search(r"/direct/([^/]+)/", cat["direct_link"]).group(1); op = session(cat["host"], tok, cat["root"])
    for i in ids:
        f = byid[i]; assert f["permission"] == "PERMISSION_DOWNLOAD", (i, f["permission"])
        out = f"{outdir}/originals/{f['name']}"
        if os.path.exists(out): print("have", out); continue
        r = op.open("https://" + cat["host"] + "/download-direct/" + str(i), timeout=900); data = r.read()
        ct = r.headers.get("Content-Type", ""); assert "html" not in ct and "json" not in ct, (i, ct, data[:200])
        open(out, "wb").write(data); print(i, f["name"], len(data), ct)
