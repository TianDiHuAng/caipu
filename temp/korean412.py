# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
for reg, lst in p["regions"].items():
    for c in lst:
        if c["slug"] == "korean":
            for cell in c["cells"]:
                if cell["target"] - cell["actual"] > 0:
                    print(cell["category"], cell["actual"], "/", cell["target"], cell["ids"])
items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
zh = {it["zh"]: it.get("aliases", []) for it in items}
for w in ["鸡", "整鸡", "鸡腿", "明太鱼", "鳕鱼", "人参", "红枣", "栗子", "糯米", "大蒜", "大葱", "辣椒酱", "韩式大酱", "绿豆芽", "牛肉", "牛腩", "海带", "鱼饼", "年糕", "白菜", "胡萝卜"]:
    print(("OK " if w in zh else "MISS ") + w)
