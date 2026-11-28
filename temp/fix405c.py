# -*- coding: utf-8 -*-
import json, os
base = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\french"
def load(n): return json.load(open(os.path.join(base, n + ".json"), encoding="utf-8"))
def save(n, d): json.dump(d, open(os.path.join(base, n + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def walk(d, pairs):
    # 替换 steps/tips/mistakes/variations/origin/serving/storage/substitutions 中文本
    for s in d["steps"]:
        for a, b in pairs:
            s["text"] = s["text"].replace(a, b); s["tip"] = s["tip"].replace(a, b); s["visual_cue"] = s["visual_cue"].replace(a, b)
    for k in ("tips", "common_mistakes", "variations", "food_safety_notes"):
        if isinstance(d.get(k), list):
            for i, it in enumerate(d[k]):
                if isinstance(it, dict) and "text" in it:
                    for a, b in pairs: it["text"] = it["text"].replace(a, b)
    for k in ("origin_note", "serving_suggestion", "storage_notes"):
        if isinstance(d.get(k), str):
            for a, b in pairs: d[k] = d[k].replace(a, b)
    if isinstance(d.get("substitutions"), list):
        for it in d["substitutions"]:
            for f in ("original", "substitute", "note"):
                if f in it:
                    for a, b in pairs: it[f] = it[f].replace(a, b)

# 1) bisque：统一为「虾」
d = load("french-bisque-de-crevettes")
for g in d["ingredients"]:
    if g["group"] == "main":
        for it in g["items"]:
            if it["name_zh"] == "虾仁": it["name_zh"] = "虾"; it["name_en"] = "shrimp"
walk(d, [("虾的外壳", "虾壳"), ("虾仁", "虾")])
save("french-bisque-de-crevettes", d)

# 2) boeuf-carottes：牛腩 -> 牛肉
d = load("french-boeuf-carottes")
walk(d, [("牛腩", "牛肉")])
save("french-boeuf-carottes", d)

# 3) pain-aux-noix：面包 -> 欧包
d = load("french-pain-aux-noix")
walk(d, [("面包房", "烘焙房"), ("面包", "欧包"), ("成品才蓬松不实", "面团才蓬松不实")])
save("french-pain-aux-noix", d)
print("fixed")
