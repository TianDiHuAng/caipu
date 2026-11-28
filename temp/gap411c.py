# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
rows = []
for reg, lst in p["regions"].items():
    for c in lst:
        gap = c["target"] - c["actual"]
        if gap > 0:
            rows.append((gap, c["slug"], c["zh"], c["actual"], c["target"]))
rows.sort(reverse=True)
for r in rows[:15]:
    print(r)
print("--- cells detail for top2")
top = [r[1] for r in rows[:2]]
for reg, lst in p["regions"].items():
    for c in lst:
        if c["slug"] in top:
            print(c["zh"], c["slug"])
            for cell in c["cells"]:
                g = cell["target"] - cell["actual"]
                if g > 0:
                    print("   ", cell["category"], cell["kind"], "gap", g, "have", cell["actual"])
