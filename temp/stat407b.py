# -*- coding: utf-8 -*-
import json, io
p = r"E:\ai_project\marvis_project\caipu\tasks\progress.json"
d = json.load(io.open(p, encoding="utf-8"))
r0 = d["regions"][0]
print("region keys:", list(r0.keys()))
print(json.dumps(r0, ensure_ascii=False)[:400])
