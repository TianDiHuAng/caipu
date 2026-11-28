# -*- coding: utf-8 -*-
import json, os, glob, io
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-410.json")
D = json.load(io.open(p, encoding="utf-8"))

items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
names = set()
for it in items:
    names.add(it["zh"])
    for a in it.get("aliases", []):
        names.add(a)

exist = set()
for f in glob.glob(os.path.join(root, "data", "recipes", "**", "*.json"), recursive=True):
    exist.add(os.path.basename(f)[:-5])
batch_ids = {r["id"] for r in D}

bad = []
for r in D:
    rid = r["id"]
    if rid in exist:
        bad.append((rid, "id_exists"))
    for i, s in enumerate(r["steps"]):
        if len(s["t"]) < 24:
            bad.append((rid, "text_short", i, len(s["t"]), s["t"]))
        if len(s["tip"]) < 19:
            bad.append((rid, "stip_short", i, len(s["tip"])))
        if len(s["cue"]) < 12:
            bad.append((rid, "cue_short", i, len(s["cue"])))
    st = sum(s["time"] for s in r["steps"] if s["heat"] != "无火")
    tot = r["prep"] + r["cook"]
    if st > tot + 5:
        bad.append((rid, "time_over", st, tot))
    for t in r["tips"]:
        if len(t) < 17:
            bad.append((rid, "tips_short", len(t)))
    for t in r["mistakes"]:
        if len(t) < 17:
            bad.append((rid, "mistakes_short", len(t)))
    for t in r["variations"]:
        if len(t) < 17:
            bad.append((rid, "variations_short", len(t)))
    if len(r["serving"]) < 20:
        bad.append((rid, "serving_short", len(r["serving"])))
    if len(r["storage"]) < 20:
        bad.append((rid, "storage_short", len(r["storage"])))
    if len(r["origin"]) < 46:
        bad.append((rid, "origin_short", len(r["origin"])))
    for x in r["related"]:
        if x not in exist and x not in batch_ids:
            bad.append((rid, "related_missing", x))
    if rid in r["related"]:
        bad.append((rid, "related_self"))
    for g in r["ingredients"]:
        for it in g["items"]:
            if len(it["note"]) < 2:
                bad.append((rid, "note_short", it["n"], it["note"]))
            if it["n"] not in names:
                bad.append((rid, "ing_unknown", it["n"]))
    main = [it for g in r["ingredients"] if g["group"] == "main" for it in g["items"]]
    for it in main:
        if it["u"] == "g" and it["a"] / r["servings"] < 60:
            bad.append((rid, "main_lt60", it["n"], round(it["a"] / r["servings"], 1)))

print("total", len(D))
for b in bad:
    print(b)
print("issues", len(bad))
