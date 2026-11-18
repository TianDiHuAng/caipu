# -*- coding: utf-8 -*-
import json, glob, os
ROOT = r"D:\AI\project\marvis_project\caipu"
t = json.loads(open(ROOT + r"\data\taxonomy.json", encoding="utf-8-sig").read())
for c in t["cuisines"]:
    print(c["slug"], "|", c["zh"], "| core:", ",".join(c.get("core", [])))
print("\ncategories:", ",".join(x["slug"] for x in t["categories"]))
print("\nexisting:")
for f in glob.glob(ROOT + r"\data\recipes\**\*.json", recursive=True):
    r = json.loads(open(f, encoding="utf-8-sig").read())
    print(" ", r["id"], r["cuisine"]["style"], r["category"])
