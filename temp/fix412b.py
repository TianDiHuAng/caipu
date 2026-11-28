# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
fp = os.path.join(root, "data", "recipes", "intl", "korean", "korean-samgyetang.json")
d = json.load(io.open(fp, encoding="utf-8"))
d["time"]["prep_min"] = 158
d["time"]["cook_min"] = 90
d["time"]["total_min"] = 248
for s in d["substitutions"]:
    s["note"] = s["note"].replace("鸡腿肉", "带骨大鸡块")
json.dump(d, io.open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(d["time"])
