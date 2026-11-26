# -*- coding: utf-8 -*-
import json, io, os, glob
os.chdir(r"E:\ai_project\marvis_project\caipu")
allr = json.load(io.open("temp/drafts/batch-327.json",encoding="utf-8"))
print("loaded", len(allr))

ing = json.load(io.open("data/ingredients.json",encoding="utf-8"))
nm = {}
for it in ing["items"]:
    for k in [it["zh"]]+(it.get("aliases") or []): nm[k]=it["zh"]

probs = []
for r in allr:
    tot = r["prep"] + r["cook"]
    st = sum(s["time"] for s in r["steps"])
    if st > tot: probs.append((r["id"],"步骤时长合计>总时长",st,tot))
    for s in r["steps"]:
        if len(s["t"]) < 21: probs.append((r["id"],"STEP短",len(s["t"]),s["t"][:20]))
        if len(s["tip"]) < 17: probs.append((r["id"],"TIP短",len(s["tip"])))
        if len(s["cue"]) < 10: probs.append((r["id"],"CUE短",len(s["cue"]),s["cue"]))
    for t in r["tips"]:
        if len(t) < 15: probs.append((r["id"],"TIPS短",len(t)))
    for t in r["mistakes"]:
        if len(t) < 17: probs.append((r["id"],"MISTAKE短",len(t)))
    if len(r["origin"]) < 46: probs.append((r["id"],"ORIGIN短",len(r["origin"])))
    if len(r["serving"]) < 20: probs.append((r["id"],"SERVING短",len(r["serving"])))
    if len(r["storage"]) < 20: probs.append((r["id"],"STORAGE短",len(r["storage"])))
    for v in r["variations"]:
        if len(v) < 17: probs.append((r["id"],"VAR短",len(v)))
    # 主料每份
    mg = 0
    for g in r["ingredients"]:
        if g["group"]=="main":
            for i in g["items"]:
                if i["u"]=="g": mg += i["a"]
    if mg/r["servings"] < 60: probs.append((r["id"],"主料每份<60g",round(mg/r["servings"],1)))
    # 食材登记
    for g in r["ingredients"]:
        for i in g["items"]:
            if i["n"] not in nm: probs.append((r["id"],"未登记食材",i["n"]))
    # 油量
    oil = 0
    for g in r["ingredients"]:
        for i in g["items"]:
            if "油" in i["n"] and i["u"]=="ml": oil += i["a"]
    lim = 45*r["servings"]
    if oil > lim: probs.append((r["id"],"油超限",oil,lim))
    # 配料是否在步骤/tips中出现
    txt = " ".join([s["t"] for s in r["steps"]] + [s["tip"] for s in r["steps"]] + r["tips"])
    for g in r["ingredients"]:
        for i in g["items"]:
            if i["n"] not in txt: probs.append((r["id"],"配料未被使用",i["n"]))
for p in probs: print(p)
print("问题数", len(probs))
