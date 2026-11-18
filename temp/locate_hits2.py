# -*- coding: utf-8 -*-
import json, glob, os
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
root = r"D:\AI\project\marvis_project\caipu\data\recipes"
items = d["items"]
namemap = []
for x in items:
    for a in [x["zh"]] + list(x.get("aliases") or []):
        if len(a) >= 2:
            namemap.append((a, x["key"]))
namemap.sort(key=lambda t: -len(t[0]))

for f in glob.glob(os.path.join(root, "**", "*.json"), recursive=True):
    r = json.loads(open(f, encoding="utf-8-sig").read())
    declared = set()
    for grp in r["ingredients"]:
        for it in grp["items"]:
            declared.add(it["name"])
            if it.get("name_en"):
                declared.add(it["name_en"])
    text = ""
    for s in r["steps"]:
        text += s["text"] + "|" + (s.get("tip") or "") + "|" + (s.get("visual_cue") or "") + "|"
    for t in (r.get("tips") or []):
        text += t + "|"
    hits = {}
    for name, key in namemap:
        if name in text:
            if any(name in dn or dn in name for dn in declared):
                continue
            idx = text.find(name)
            hits.setdefault(name, text[max(0, idx - 15):idx + 18])
    if hits:
        print("==", r["id"])
        for k, v in hits.items():
            print("   ", k, "::", v)
