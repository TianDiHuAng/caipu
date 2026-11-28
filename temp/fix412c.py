# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
fp = os.path.join(root, "data", "recipes", "intl", "korean", "korean-samgyetang.json")
d = json.load(io.open(fp, encoding="utf-8"))
for s in d["steps"]:
    s["text"] = s["text"].replace("把鸡腿交叉绑住", "把两条腿交叉绑住").replace("鸡腿并拢绑紧", "两腿并拢绑紧")
json.dump(d, io.open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print([s["text"] for s in d["steps"] if "绑" in s["text"] or "腿" in s["text"]])
