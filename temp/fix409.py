# -*- coding: utf-8 -*-
import json, os, sys, runpy
root = r"E:\ai_project\marvis_project\caipu"
os.chdir(root)
sys.path.insert(0, os.path.join(root, "temp"))
g = runpy.run_path(os.path.join(root, "temp", "gen409.py"))
D = g["D"]
import patch409_data as P
import patch409b as P2
import patch409c as P3
P.CUE.update(P2.CUE2)
P.CUE.update(P3.CUE3)

for r in D:
    for i, s in enumerate(r["steps"]):
        if (r["id"], i) in P.CUE: s["cue"] = P.CUE[(r["id"], i)]
        if (r["id"], i) in P.TIP: s["tip"] = P.TIP[(r["id"], i)]
        if (r["id"], i) in P.TEXT: s["t"] = P.TEXT[(r["id"], i)]

probs = []
for r in D:
    for i, s in enumerate(r["steps"]):
        if len(s["t"]) < 23: probs.append((r["id"], "text短", i, len(s["t"])))
        if len(s["tip"]) < 18: probs.append((r["id"], "tip短", i, len(s["tip"])))
        if len(s["cue"]) < 12: probs.append((r["id"], "cue短", i, len(s["cue"])))
    tot = sum(s["time"] for s in r["steps"])
    if tot > r["prep"] + r["cook"]: probs.append((r["id"], "时长超", tot, r["prep"] + r["cook"]))
print("问题数", len(probs))
for p_ in probs: print(p_)
if not probs:
    out = os.path.join(root, "temp", "drafts", "batch-409.json")
    json.dump(D, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("已写", out, len(D))
