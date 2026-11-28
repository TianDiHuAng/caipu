# -*- coding: utf-8 -*-
import json, io, os, glob
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
target = "taiwan"
rows = []

def dig(o):
    if isinstance(o, dict):
        if o.get("slug") == target and "cells" in o:
            rows.append(o)
        for v in o.values():
            dig(v)
    elif isinstance(o, list):
        for v in o:
            dig(v)

dig(p["regions"])
if rows:
    c = rows[0]
    print("cuisine", c.get("slug"), c.get("actual"), c.get("target"))
    for cell in c.get("cells", []):
        if cell.get("actual", 0) < cell.get("target", 0):
            print(" 缺", cell.get("slug") or cell.get("category"), cell.get("actual"), cell.get("target"))

ids = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(root, "data", "recipes", "cn", target, "*.json"))]
print("现有", len(ids))
print(sorted(ids))
