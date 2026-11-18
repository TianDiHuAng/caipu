# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
items = d["items"]
keys = {x["key"] for x in items}
new = [
    {"key": "salt-pork", "zh": "咸肉", "en": "salt-cured pork belly",
     "aliases": ["咸肉", "腌肉", "金华咸肉", "咸五花肉"], "allergens": [], "category": "meat"},
    {"key": "tofu-skin-knot", "zh": "百叶结", "en": "tofu skin knot",
     "aliases": ["百叶结", "千张结"], "allergens": ["soy"], "category": "soy"},
]
added = []
for n in new:
    if n["key"] in keys:
        print("skip exists", n["key"])
        continue
    items.append(n)
    added.append(n["key"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", added, "total", len(items))
