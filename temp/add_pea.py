# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
zhs = {x["zh"] for x in d["items"]}
keys = {x["key"] for x in d["items"]}
add = [{"key": "green-pea", "zh": "豌豆", "en": "green pea", "aliases": ["青豆", "豌豆粒"], "allergens": [], "category": "vegetable"}]
for n in add:
    if n["key"] in keys or n["zh"] in zhs:
        print("skip", n["key"]); continue
    d["items"].append(n); print("added", n["key"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
m = {}
for x in d["items"]:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        m.setdefault(a, []).append(x["key"])
print("dup:", {k: v for k, v in m.items() if len(v) > 1}, "total", len(d["items"]))
