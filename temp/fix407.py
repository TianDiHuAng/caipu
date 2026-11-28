# -*- coding: utf-8 -*-
import json, io
p = r"E:\ai_project\marvis_project\caipu\temp\drafts\batch-407.json"
D = json.load(io.open(p, encoding="utf-8"))
for r in D:
    if r["id"] == "taiwan-yuyuan":
        r["flavor"] = ["sweet", "rich", "fragrant"]
    if r["id"] == "taiwan-caipudan":
        r["diet"] = [x for x in r["diet"] if x != "gluten-free"]
    if r["id"] == "taiwan-jinsha-kugua":
        for s in r["steps"]:
            if "咸蛋黄末" in s["t"]:
                s["t"] = s["t"].replace("小火下咸蛋黄末", "小火下蒜末和咸蛋黄末")
r["overwrite"] = True
for r in D:
    r["overwrite"] = True
json.dump(D, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done", len(D))
