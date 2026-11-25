# -*- coding: utf-8 -*-
import json, os, collections
os.chdir(r"E:\ai_project\marvis_project\caipu")
pg = json.load(open("tasks/progress.json", encoding="utf-8"))
print(type(pg), list(pg.keys())[:10] if isinstance(pg, dict) else len(pg))
def walk(o, depth=0):
    if isinstance(o, dict):
        for k in list(o.keys())[:6]:
            print("  " * depth + str(k), type(o[k]).__name__)
            if depth < 2: walk(o[k], depth + 1)
walk(pg)
