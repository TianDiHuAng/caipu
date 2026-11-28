# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
want = ["鸡蛋", "胡萝卜", "洋葱", "小葱", "豆腐", "黄豆芽", "豆芽", "土豆", "白萝卜", "韭菜", "白芝麻",
        "香油", "酱油", "大蒜", "辣椒粉", "辣椒酱", "泡菜", "醋", "白糖", "盐", "植物油", "黄油",
        "黑胡椒", "西葫芦", "蕨菜", "桔梗", "黄瓜", "鹌鹑蛋", "海苔", "糯米粉", "面粉", "清水", "熟芝麻",
        "干香菇", "香菇", "糯米", "大酱", "鱼露"]
zh = {}
for it in items:
    zh[it["zh"]] = it.get("aliases", [])
for w in want:
    if w in zh:
        print("OK", w, "|aliases:", ",".join(zh[w][:6]))
    else:
        hit = [k for k in zh if w in k or k in w]
        print("MISS", w, "-> near", hit[:5])
