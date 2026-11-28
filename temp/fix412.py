# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
fp = os.path.join(root, "data", "recipes", "intl", "korean", "korean-samgyetang.json")
d = json.load(io.open(fp, encoding="utf-8"))
d["related_ids"] = ["korean-galbi-jjim", "korean-dakdoritang", "korean-doenjang-jjigae"]
json.dump(d, io.open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(d["related_ids"])
