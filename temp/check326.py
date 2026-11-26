# -*- coding: utf-8 -*-
import json, io, os, glob
os.chdir(r"E:\ai_project\marvis_project\caipu")
d=json.load(io.open("temp/drafts/batch-326.json",encoding="utf-8"))
ing=json.load(io.open("data/ingredients.json",encoding="utf-8"))
names=set()
for it in ing["items"]:
    names.add(it["zh"])
    for al in it.get("aliases",[]) or []:
        names.add(al)
existing=set()
for p in glob.glob("data/recipes/**/*.json",recursive=True):
    existing.add(os.path.basename(p)[:-5])

probs=[]
for r in d:
    if r["id"] in existing: probs.append("%s 已存在"%r["id"])
    for s in r["steps"]:
        if len(s["t"])<21: probs.append("%s step短(%d):%s"%(r["id"],len(s["t"]),s["t"][:12]))
        if len(s["tip"])<17: probs.append("%s tip短:%s"%(r["id"],s["tip"][:10]))
        if len(s["cue"])<10: probs.append("%s cue短:%s"%(r["id"],s["cue"]))
    for i in r["tips"]:
        if len(i)<15: probs.append("%s tips单条短:%s"%(r["id"],i))
    for i in r["mistakes"]:
        if len(i)<15: probs.append("%s mistakes单条短:%s"%(r["id"],i))
    for i in r["variations"]:
        if len(i)<17: probs.append("%s variations短:%s"%(r["id"],i))
    if len(r["serving"])<20: probs.append("%s serving短(%d)"%(r["id"],len(r["serving"])))
    if len(r["storage"])<20: probs.append("%s storage短(%d)"%(r["id"],len(r["storage"])))
    if len(r["origin"])<46: probs.append("%s origin短(%d)"%(r["id"],len(r["origin"])))
    # 食材登记
    for g in r["ingredients"]:
        for i in g["items"]:
            if i["n"] not in names: probs.append("%s 未登记食材:%s"%(r["id"],i["n"]))
            if len(i["note"])<2: probs.append("%s note短:%s"%(r["id"],i["n"]))
    # 油量
    oil=sum(i["a"] for g in r["ingredients"] if g["group"]=="seasoning" for i in g["items"] if "油" in i["n"] and i["u"]=="ml")
    if oil>45*r["servings"]: probs.append("%s 油量%d 超非炸上限%d"%(r["id"],oil,45*r["servings"]))
print("问题数",len(probs))
for p in probs: print(p)
