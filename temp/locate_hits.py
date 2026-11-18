# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["key"] == "welsh-onion":
        x["aliases"] = ["京葱", "葱丝", "葱白", "葱段"]
        print("welsh-onion aliases:", x["aliases"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 定位脚本：输出所有菜谱中出现的、未在配料表中声明的食材词及其上下文
import glob, os, re
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
    for g, arr in r["ingredients"].items():
        for it in arr:
            declared.add(it["name"])
            if it.get("name_en"):
                declared.add(it["name_en"])
    text = ""
    for s in r["steps"]:
        text += s["text"] + "|" + s.get("tip", "") + "|" + s.get("visual_cue", "") + "|"
    for t in r.get("tips") or []:
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
