# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
items = d["items"]
zhs = {x["zh"] for x in items}
keys = {x["key"] for x in items}
new = [
    {"key": "beef-tripe", "zh": "牛肚", "en": "beef tripe", "aliases": ["毛肚", "牛百叶"], "allergens": [], "category": "meat"},
    {"key": "pork-intestine", "zh": "猪大肠", "en": "pork large intestine", "aliases": ["肥肠", "大肠"], "allergens": [], "category": "meat"},
    {"key": "mandarin-fish", "zh": "鳜鱼", "en": "mandarin fish", "aliases": ["桂鱼", "鳜鱼条"], "allergens": ["fish"], "category": "seafood"},
    {"key": "river-shrimp", "zh": "河虾仁", "en": "river shrimp", "aliases": ["虾仁", "河虾", "鲜虾仁"], "allergens": ["crustacean"], "category": "seafood"},
    {"key": "pine-nut", "zh": "松子仁", "en": "pine nut", "aliases": ["松仁", "松子"], "allergens": ["nut"], "category": "nut"},
    {"key": "dried-chili", "zh": "干辣椒", "en": "dried red chili", "aliases": ["干辣椒段"], "allergens": [], "category": "vegetable"},
    {"key": "rock-sugar", "zh": "冰糖", "en": "rock sugar", "aliases": ["黄冰糖", "单晶冰糖"], "allergens": [], "category": "other"},
    {"key": "longjing-tea", "zh": "龙井茶", "en": "Longjing tea", "aliases": ["龙井", "西湖龙井"], "allergens": [], "category": "other"},
]
added = []
for n in new:
    if n["key"] in keys or n["zh"] in zhs:
        print("skip", n["key"])
        continue
    items.append(n)
    added.append(n["key"])
m = {}
for x in items:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        m.setdefault(a, []).append(x["key"])
dup = {k: v for k, v in m.items() if len(v) > 1}
print("dup:", dup)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", added, "total", len(items))
