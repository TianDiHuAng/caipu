# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
items = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
words = ["高丽菜", "卷心菜", "包菜", "丝瓜", "苦瓜", "咸蛋", "咸鸭蛋", "鸭蛋", "鲈鱼", "豆瓣酱", "豆酱",
         "沙茶酱", "鱿鱼", "菜脯", "萝卜干", "糯米", "香菇", "虾米", "芋头", "地瓜粉", "木薯粉", "米酒",
         "芝麻油", "麻油", "老姜", "枸杞", "蒜蓉", "酱油膏", "香菜", "红葱头", "五花肉", "鸡腿", "肉桂",
         "冰糖", "白胡椒", "豆芽", "韭菜", "空心菜", "地瓜叶", "笋", "竹笋", "咸蛋黄", "鸡蛋", "虾仁"]
for w in words:
    hit = [i["zh"] + (("/" + ",".join(i.get("aliases", []))) if i.get("aliases") else "") for i in items if w == i["zh"] or w in i.get("aliases", []) or w in i["zh"]]
    print(w, "=>", hit[:3])
