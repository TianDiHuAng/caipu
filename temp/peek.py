# -*- coding: utf-8 -*-
import json, io
p = r"E:\ai_project\marvis_project\caipu\data\recipes\cn\hakka\kejia-suan-luobo.json"
d = json.load(io.open(p, encoding="utf-8"))
print(d.get("prep_min"), d.get("cook_min"), d.get("time"))
for s in d["steps"]:
    print(s["time_min"], s["heat"], s["text"][:34])
