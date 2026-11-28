# -*- coding: utf-8 -*-
import json, io, os, re, glob
root = r"E:\ai_project\marvis_project\caipu"
D = json.load(io.open(os.path.join(root, "temp", "drafts", "batch-411.json"), encoding="utf-8"))
items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
names, alias = set(), {}
for it in items:
    names.add(it["zh"])
    for a in it.get("aliases", []):
        alias[a] = it["zh"]

FL = {"light","savory","umami","salty","sour","spicy","fragrant","rich","sweet","tangy","smoky","bitter","herbal"}
DIET = {"vegetarian","vegan","gluten-free","dairy-free","halal","kosher","low-carb","high-protein","pescatarian"}
UNIT = {"g","ml","piece","tbsp","tsp"}
def nolen(x): return len(re.sub(r"\s", "", x))

issues = []
ids = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root, "data", "recipes", "*", "*", "*.json"))}
ids |= {r["id"] for r in D}
for r in D:
    p = r["id"]
    for f in r["flavor"]:
        if f not in FL: issues.append((p, "flavor " + f))
    for d in r["diet"]:
        if d not in DIET: issues.append((p, "diet " + d))
    for g in r["ingredients"]:
        for it in g["items"]:
            if it["u"] not in UNIT: issues.append((p, "unit " + it["u"]))
            if it["n"] not in names and it["n"] not in alias:
                issues.append((p, "ing not registered: " + it["n"]))
            if nolen(it["note"]) < 2: issues.append((p, "ing note short " + it["n"]))
    tot = sum(it["a"] for g in r["ingredients"] if g["group"] == "main" for it in g["items"])
    if tot / r["servings"] < 60: issues.append((p, "main g/serv %0.f" % (tot / r["servings"])))
    totsteps = 0
    for s in r["steps"]:
        if nolen(s["t"]) < 23: issues.append((p, "text short: " + s["t"][:14]))
        if nolen(s["tip"]) < 18: issues.append((p, "tip short: " + s["tip"][:12]))
        if nolen(s["cue"]) < 11: issues.append((p, "cue short: " + s["cue"][:12]))
        if s["heat"] not in ("无火","小火","中小火","中火","中大火","大火"): issues.append((p,"heat "+s["heat"]))
        if s["heat"] != "无火": totsteps += s["time"]
    total = r["prep"] + r["cook"]
    if totsteps > total * 2 + 10: issues.append((p, "step time %d > total %d" % (totsteps, total)))
    for t in r["tips"]:
        if nolen(t) < 17: issues.append((p, "tips short: " + t[:12]))
    for m in r["mistakes"]:
        if nolen(m) < 17: issues.append((p, "mistake short: " + m[:12]))
    if nolen(r["serving"]) < 20: issues.append((p, "serving short"))
    if nolen(r["storage"]) < 20: issues.append((p, "storage short"))
    if nolen(r["origin"]) < 46: issues.append((p, "origin short"))
    for v in r["variations"]:
        if nolen(v) < 17: issues.append((p, "variation short"))
    if not r["equipment"]: issues.append((p, "no equip"))
    for rid in r["related"]:
        if rid == p: issues.append((p, "related self"))
        elif rid not in ids: issues.append((p, "related missing " + rid))
    if len(r["steps"]) < 7: issues.append((p, "steps < 7"))
    txt = " ".join(r.get("safety", []))
    allnames = [it["n"] for g in r["ingredients"] for it in g["items"]]
    if [n for n in allnames if n in ("鸡蛋","黄豆芽","香菇","泡菜","北豆腐")] and not any(
            k in txt for k in ("安全","彻底加热","中心温度","熟透","不要生食","冷藏")):
        issues.append((p, "safety word missing"))
print("issues", len(issues))
for i in issues: print(i)
