# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
items = d["items"]
keys = {x["key"] for x in items}
new = [
    {"key": "potato-starch", "zh": "土豆淀粉", "en": "potato starch",
     "aliases": ["土豆淀粉", "生粉", "太白粉"], "allergens": [], "category": "grain"},
]
added = []
alias_map = {}
for x in items:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        alias_map.setdefault(a, []).append(x["key"])
for n in new:
    if n["key"] in keys:
        print("skip exists", n["key"])
        continue
    for a in [n["zh"]] + list(n["aliases"]):
        if a in alias_map:
            print("WARN alias conflict", a, alias_map[a])
    items.append(n)
    added.append(n["key"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", added, "total", len(items))
