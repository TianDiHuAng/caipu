# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
a=json.load(io.open("temp/drafts/batch-326.json",encoding="utf-8"))
b=json.load(io.open("temp/drafts/batch-326b.json",encoding="utf-8"))
c=json.load(io.open("temp/drafts/batch-326c.json",encoding="utf-8"))
out=a+b+c
for r in out:
    r["overwrite"]=True
json.dump(out, io.open("temp/drafts/batch-326.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("merged",len(out))
for r in out:
    s=sum(x["time"] for x in r["steps"])
    main=sum(i["a"] for g in r["ingredients"] if g["group"]=="main" for i in g["items"] if i["u"] in ("g","ml"))
    print(r["id"], "sum=%d budget=%d"%(s, r["prep"]+r["cook"]), "mainPerSrv=%.0f"%(main/r["servings"]), "steps=%d"%len(r["steps"]))
