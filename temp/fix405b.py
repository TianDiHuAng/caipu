# -*- coding: utf-8 -*-
import json, os
base = r"E:\ai_project\marvis_project\caipu"
dp = os.path.join(base, "temp", "drafts", "batch-405.json")
arr = json.load(open(dp, encoding="utf-8"))
for r in arr:
    if r["id"] == "french-fougasse":
        for g in r["ingredients"]:
            g["items"] = [i for i in g["items"] if i["n"] != "粗盐"]
        for s in r["steps"]:
            s["t"] = s["t"].replace("撒粗盐", "撒少许盐")
        r["related"] = ["french-pain-de-campagne", "french-brioche"]
    if r["id"] == "french-pain-aux-noix":
        r["related"] = ["french-pain-de-campagne", "french-brioche"]
        r["tips"] = [t.replace("面包", "成品") for t in r["tips"]]
        for s in r["steps"]:
            s["t"] = s["t"].replace("面包才蓬松不实", "面团才蓬松不实")
    if r["id"] == "french-boeuf-carottes":
        for s in r["subs"]:
            if s["orig"] == "牛腩":
                s["orig"] = "牛肉"; s["sub"] = "牛肩肉"
    if r["id"] == "french-bisque-de-crevettes":
        for s in r["steps"]:
            s["t"] = s["t"].replace("虾壳", "虾的外壳")
json.dump(arr, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("draft fixed", len(arr))
