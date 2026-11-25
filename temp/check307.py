# -*- coding: utf-8 -*-
import json, sys, glob, os

os.chdir(r"E:\ai_project\marvis_project\caipu")
files = sys.argv[1:] or ["temp/drafts/batch-307.json"]
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    for r in data:
        errs = []
        for i, s in enumerate(r["steps"]):
            if len(s["t"]) < 21: errs.append("step%d t=%d" % (i, len(s["t"])))
            if len(s["tip"]) < 17: errs.append("step%d tip=%d" % (i, len(s["tip"])))
            if len(s["cue"]) < 10: errs.append("step%d cue=%d" % (i, len(s["cue"])))
        for ti, x in enumerate(r["tips"]):
            if len(x) < 17: errs.append("tip%d=%d" % (ti, len(x)))
        for mi, x in enumerate(r["mistakes"]):
            if len(x) < 17: errs.append("mis%d=%d" % (mi, len(x)))
        for vi, x in enumerate(r["variations"]):
            if len(x) < 17: errs.append("var%d=%d" % (vi, len(x)))
        for si, x in enumerate(r["safety"]):
            if len(x) < 17: errs.append("saf%d=%d" % (si, len(x)))
        if len(r["serving"]) < 20: errs.append("serving=%d" % len(r["serving"]))
        if len(r["storage"]) < 20: errs.append("storage=%d" % len(r["storage"]))
        if len(r["origin"]) < 46: errs.append("origin=%d" % len(r["origin"]))
        st = sum(s["time"] for s in r["steps"])
        if st > r["prep"] + r["cook"]:
            errs.append("timesum %d>%d" % (st, r["prep"] + r["cook"]))
        if abs(r["prep"] + r["cook"] - r["prep"] - r["cook"]) > 5:
            pass
        mainamt = sum(i["a"] for i in r["ingredients"][0]["items"]) / r["servings"]
        if mainamt < 60: errs.append("main=%.0f" % mainamt)
        oil = 0
        for g in r["ingredients"]:
            for it in g["items"]:
                if "油" in it["n"] and it["u"] == "ml":
                    oil += it["a"]
        print("%-28s oil=%d main=%.0f %s" % (r["id"], oil, mainamt, errs if errs else "OK"))
