# -*- coding: utf-8 -*-
import json
p = json.load(open(r"E:\ai_project\marvis_project\caipu\tasks\progress.json", encoding="utf-8"))
gaps = []
for reg in p["regions"]:
    for cu in reg["cuisines"]:
        miss = {}
        for c in cu["cells"]:
            d = c["target"] - c["actual"]
            if d > 0:
                miss[c["category"]] = d
        if miss:
            gaps.append((sum(miss.values()), cu["slug"], miss))
gaps.sort(key=lambda x: -x[0])
for g in gaps[:12]:
    print(g)
print("总缺口", sum(g[0] for g in gaps))
