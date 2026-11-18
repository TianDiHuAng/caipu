# -*- coding: utf-8 -*-
import json, io, sys
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
raw = open(p, encoding="utf-8-sig").read()
d = json.loads(raw)
arr = d["ingredients"] if isinstance(d, dict) and "ingredients" in d else d
print("total", len(arr))
print("keys sample", list(arr[0].keys()))
for x in arr:
    blob = json.dumps(x, ensure_ascii=False)
    if any(s in blob for s in ["cured", "腌", "豆皮", "百叶", "豆腐皮", "tofu-skin", "tofu skin"]):
        print(x.get("key"), "|", x.get("zh"), "|", x.get("en"), "|", x.get("category"), "|", x.get("allergens"))
