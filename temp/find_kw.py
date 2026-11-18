# -*- coding: utf-8 -*-
import json, os
BASE = r"D:\AI\project\marvis_project\caipu\data\recipes"
for rid in ("jiuzhuan-dachang", "fuqi-feipian"):
    for root, _, files in os.walk(BASE):
        if rid + ".json" in files:
            p = os.path.join(root, rid + ".json")
            r = json.loads(open(p, encoding="utf-8-sig").read())
            for s in r["steps"]:
                for kw in ("肥牛", "面粉"):
                    if kw in s["text"]:
                        i = s["text"].index(kw)
                        print(rid, kw, "|", s["text"][max(0, i-25):i+25])
            for s in r["steps"]:
                for kw in ("肥牛", "面粉"):
                    for f in ("tip", "visual_cue"):
                        if kw in s[f]:
                            i = s[f].index(kw)
                            print(rid, kw, f, "|", s[f][max(0, i-25):i+25])
