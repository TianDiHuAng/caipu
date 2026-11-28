# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
fp = os.path.join(root, "data", "ingredients.json")
data = json.load(io.open(fp, encoding="utf-8"))
items = data["items"]
zs = {it["zh"] for it in items}
al = set()
for it in items:
    for a in it.get("aliases", []):
        al.add(a)
new = {
    "key": "crayfish",
    "zh": "小龙虾",
    "en": "crayfish",
    "aliases": ["淡水小龙虾"],
    "allergens": ["crustacean"],
    "category": "seafood",
}
if new["zh"] not in zs and "淡水小龙虾" not in al:
    items.append(new)
    json.dump(data, io.open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("added", len(items))
else:
    print("exists")
