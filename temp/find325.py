# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-325.json"
d=json.load(io.open(p,encoding="utf-8"))
for r in d:
    for s in r["steps"]:
        for k in ("t","tip","cue"):
            if "面条" in s.get(k,""):
                print(r["id"],"step",k,s[k][:40])
    for i,t in enumerate(r["tips"]):
        if "面条" in t: print(r["id"],"tip",i,t[:40])
    for i,t in enumerate(r.get("variations",[])):
        if "面条" in t: print(r["id"],"var",i,t[:40])
    for i,t in enumerate(r.get("common_mistakes",[]) or []):
        if "面条" in t: print(r["id"],"mis",i,t[:40])
