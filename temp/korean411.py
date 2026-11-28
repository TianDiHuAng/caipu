# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
for reg, lst in p["regions"].items():
    for c in lst:
        if c["slug"] == "korean":
            for cell in c["cells"]:
                if cell["category"] in ("main-vegetable", "main-egg", "main-tofu", "main-meat", "soup"):
                    print(cell["category"], cell["actual"], "/", cell["target"], cell["ids"])

# 已有 korean 文件
d = os.path.join(root, "data", "recipes", "kr", "korean")
print("dirs", os.listdir(os.path.join(root, "data", "recipes", "kr")) if os.path.exists(os.path.join(root, "data", "recipes", "kr")) else "no kr")
