# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
d=json.load(io.open("data/ingredients.json",encoding="utf-8"))
items=d["items"]
for it in items:
    if it.get("zh") in ("粉丝","豆腐皮","玉米淀粉","鹅肉","猪血","酸菜","玉米面","黄豆酱"):
        print(json.dumps(it,ensure_ascii=False))
print("keys:",list(items[0].keys()))
