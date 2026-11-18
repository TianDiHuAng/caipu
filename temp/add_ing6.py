# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
items = d["items"]
keys = {x["key"] for x in items}
new = [
    {"key": "pork-ribs", "zh": "猪肋排", "en": "pork spare ribs",
     "aliases": ["肋排", "排骨", "小排"], "allergens": [], "category": "meat"},
    {"key": "onion", "zh": "洋葱", "en": "onion",
     "aliases": [], "allergens": [], "category": "vegetable"},
    {"key": "lamb-leg", "zh": "羊腿肉", "en": "lamb leg",
     "aliases": ["羊肉", "羊后腿"], "allergens": [], "category": "meat"},
]
added = []
for n in new:
    if n["key"] in keys:
        print("skip exists", n["key"])
        continue
    items.append(n)
    added.append(n["key"])
# 复查冲突
m = {}
for x in items:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        m.setdefault(a, []).append(x["key"])
print("dup aliases:", {k: v for k, v in m.items() if len(v) > 1})
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", added, "total", len(items))
