# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-412.json")
D = json.load(io.open(p, encoding="utf-8"))
for r in D:
    if r["id"] != "korean-yachae-bokkeumbap":
        continue
    for s in r["steps"]:
        if "洋葱" in s["tip"] and "炒软" in s["tip"]:
            s["tip"] = "洋葱一定要先炒到透明变软，甜味出来整锅炒饭都会更香。"
json.dump(D, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
