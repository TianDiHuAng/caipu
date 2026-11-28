# -*- coding: utf-8 -*-
import json, io, os, re
root = r"E:\ai_project\marvis_project\caipu"
D = json.load(io.open(os.path.join(root, "temp", "drafts", "batch-411.json"), encoding="utf-8"))
items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
names = set()
alias = {}
for it in items:
    names.add(it["zh"])
    for a in it.get("aliases", []):
        alias[a] = it["zh"]

FL = {"light","savory","umami","salty","sour","spicy","fragrant","rich","sweet","tangy","smoky","bitter","herbal"}
DIET = {"vegetarian","vegan","gluten-free","dairy-free","halal","kosher","low-carb","high-protein","pescatarian"}
UNIT = {"g","ml","piece","tbsp","tsp"}

def nolen(x):
    return len(re.sub(r"\s", "", x))

issues = []
import glob
ids = set()
for f in glob.glob(os.path.join(root, "data", "recipes", "*", "*", "*.json")):
    ids.add(os.path.basename(f)[:-5])
ids |= {r["id"] for r in D}

for r in D:
    p = r["id"]
    if p not in ids: issues.append((p, "id not in ids?"))
    for f in r["flavor"]:
        if f not in FL: issues.append((p, "flavor " + f))
    for d in r["diet"]:
        if d not in DIET: issues.append((p, "diet " + d))
    for g in r["ingredients"]:
        for it in g["items"]:
            if it["u"] not in UNIT: issues.append((p, "unit " + it["u"]))
            if it["n"] not in names and it["n"] not in alias:
                issues.append((p, "ing not registered: " + it["n"] + " => " + alias.get(it["n"], "?")))
            if nolen(it["note"]) < 2: issues.append((p, "ing note short " + it["n"]))
    # main grams per serving
    serv = r["servings"]
    tot = sum(it["a"] for g in r["ingredients"] if g["group"] == "main" for it in g["items"])
    if tot / serv < 60: issues.append((p, "main g/serv %.0f" % (tot/serv)))
    totsteps = 0
    for s in r["steps"]:
        if nolen(s["t"]) < 23: issues.append((p, "text short: " + s["t"][:14]))
        if nolen(s["tip"]) < 18: issues.append((p, "tip short: " + s["tip"][:12]))
        if nolen(s["cue"]) < 11: issues.append((p, "cue short: " + s["cue"][:12]))
        if s["heat"] not in ("鏃犵伀","灏忕伀","涓皬鐏?,"涓伀","涓ぇ鐏?,"澶х伀"): issues.append((p,"heat "+s["heat"]))
        if s["heat"] != "鏃犵伀": totsteps += s["time"]
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
    # high risk ingredients
    txt = " ".join(r.get("safety", []))
    allnames = [it["n"] for g in r["ingredients"] for it in g["items"]]
    risky = [n for n in allnames if n in ("楦¤泲","榛勮眴鑺?,"棣欒弴","娉¤彍","鍖楄眴鑵?)]
    if risky and not any(k in txt for k in ("瀹夊叏","褰诲簳鍔犵儹","涓績娓╁害","鐔熼€?,"涓嶈鐢熼","鍐疯棌")):
        issues.append((p, "safety word missing"))

print("issues", len(issues))
for i in issues[:40]:
    print(i)

