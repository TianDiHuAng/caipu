# -*- coding: utf-8 -*-
import json, io, os, glob
root = r"E:\ai_project\marvis_project\caipu"
tax = json.load(io.open(os.path.join(root, "data", "taxonomy.json"), encoding="utf-8"))
cuisines = {c["slug"]: c for c in tax["cuisines"]}
cats = [c["slug"] for c in tax["categories"]]

def stat(slug):
    d = os.path.join(root, "data", "recipes", "intl", slug)
    if not os.path.isdir(d):
        d = os.path.join(root, "data", "recipes", slug)
    cnt = {}
    files = glob.glob(os.path.join(d, "*.json"))
    for f in files:
        j = json.load(io.open(f, encoding="utf-8"))
        cnt[j["category"]] = cnt.get(j["category"], 0) + 1
    return len(files), cnt

for slug in ["hunan", "beijing", "french", "middle-east"]:
    n, cnt = stat(slug)
    c = cuisines.get(slug)
    print(slug, "total", n, c.get("target") if c else None, "core", c.get("core_categories") if c else None)
    print("   ", cnt)
