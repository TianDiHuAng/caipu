# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
print("top keys", list(d.keys()))
for k, v in d.items():
    print(k, type(v), (len(v) if hasattr(v, "__len__") else ""))
# find actual list
lst = None
for k, v in d.items():
    if isinstance(v, list) and v and isinstance(v[0], dict):
        lst = v
        print("list key", k, "sample keys", list(v[0].keys())[:12])
        break
if lst:
    for x in lst:
        blob = json.dumps(x, ensure_ascii=False)
        if any(s in blob for s in ["cured", "腌", "豆皮", "百叶", "豆腐皮", "tofu-skin", "tofu skin"]):
            print(x.get("key") or x.get("slug"), "|", x.get("zh"), "|", x.get("en"), "|", x.get("category"), "|", x.get("allergens"))
