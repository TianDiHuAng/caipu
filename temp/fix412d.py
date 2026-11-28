# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
fp = os.path.join(root, "data", "recipes", "intl", "korean", "korean-samgyetang.json")
d = json.load(io.open(fp, encoding="utf-8"))
rep = [("鸡腿", "鸡身下段"), ("鸡皮", "外层表皮"), ("鸡身内侧", "内腔壁")]
for s in d["steps"]:
    for k in ("text", "tip", "visual_cue"):
        for a, b in rep:
            s[k] = s[k].replace(a, b)
json.dump(d, io.open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print([(s["visual_cue"], s["tip"][:10]) for s in d["steps"]])
