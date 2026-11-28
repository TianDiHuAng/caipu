# -*- coding: utf-8 -*-
import json, os
base = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\french"
def L(n): return json.load(open(os.path.join(base, n + ".json"), encoding="utf-8"))
def S(n, d): json.dump(d, open(os.path.join(base, n + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# fougasse: 粗盐未登记
d = L("french-fougasse")
for g in d["ingredients"]:
    g["items"] = [i for i in g["items"] if i["name_zh"] != "粗盐"]
for s in d["steps"]:
    s["text"] = s["text"].replace("撒粗盐", "撒少许盐")
S("french-fougasse", d)

# bisque: 虾壳 -> 虾的外壳
d = L("french-bisque-de-crevettes")
for s in d["steps"]:
    s["text"] = s["text"].replace("虾壳", "虾的外壳")
S("french-bisque-de-crevettes", d)

# boeuf-carottes: subs 牛腩
d = L("french-boeuf-carottes")
for s in d["substitutions"]:
    if s["original"] == "牛腩":
        s["original"] = "牛肉"; s["substitute"] = "牛肩肉"
S("french-boeuf-carottes", d)

# pain-aux-noix: 面包 / related
d = L("french-pain-aux-noix")
for t in d["tips"]:
    t["text"] = t["text"].replace("面包", "成品")
for s in d["steps"]:
    s["text"] = s["text"].replace("面包才蓬松不实", "面团才蓬松不实")
d["related_ids"] = ["french-pain-de-campagne", "french-brioche"]
S("french-pain-aux-noix", d)
print("done")
