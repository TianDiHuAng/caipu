# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
# 1) 登记新食材
p="data/ingredients.json"
d=json.load(io.open(p,encoding="utf-8"))
items=d["items"]
existing=set()
for it in items:
    existing.add(it["zh"])
    for a in it.get("aliases",[]) or []:
        existing.add(a)
new=[
 {"key":"dried-sweet-potato-noodles","zh":"粉条","en":"dried sweet potato noodles","aliases":["宽粉","红薯粉条"],"allergens":[],"category":"grain"},
 {"key":"pressed-tofu","zh":"干豆腐","en":"pressed tofu","aliases":["东北干豆腐"],"allergens":["soy"],"category":"soy"},
 {"key":"blood-sausage","zh":"血肠","en":"blood sausage","aliases":["东北血肠"],"allergens":[],"category":"meat"},
]
add=[n for n in new if n["zh"] not in existing and not any(a in existing for a in n["aliases"])]
items.extend(add)
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("added",[a["zh"] for a in add],"total",len(items))
print(json.dumps(json.load(io.open("temp/drafts/batch-325.json",encoding="utf-8"))[0],ensure_ascii=False)[:2500])
