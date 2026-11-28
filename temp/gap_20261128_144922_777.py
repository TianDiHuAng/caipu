# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
print("totals", p["totals"])
rows = []

def dig(o):
    if isinstance(o, dict):
        if "slug" in o and "actual" in o and "target" in o:
            rows.append((o["target"] - o["actual"], o["slug"], o["actual"], o["target"]))
            return
        for v in o.values():
            dig(v)
    elif isinstance(o, list):
        for v in o:
            dig(v)

dig(p["regions"])
rows.sort(reverse=True)
print("缺口TOP", rows[:12])
print("已达标数", sum(1 for r in rows if r[0] <= 0), "总菜系", len(rows))
