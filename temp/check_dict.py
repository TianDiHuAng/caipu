# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
items = json.load(open("data/ingredients.json", encoding="utf-8"))["items"]
names = set()
alias = {}
for it in items:
    names.add(it["zh"])
    for a in it.get("aliases", []):
        alias.setdefault(a, it["zh"])
check = ["菠菜", "韭黄", "绿豆芽", "花生米", "紫菜", "鸡腿肉", "老豆腐", "嫩豆腐", "白菜", "粉丝",
         "胡萝卜", "香菇", "鸡蛋", "香菜", "熟白芝麻", "白胡椒粉", "蚝油", "老抽", "高汤",
         "皮蛋", "海带", "青椒", "尖椒", "黄瓜", "大白菜", "土豆", "干辣椒", "花椒"]
for c in check:
    print("%-8s %s" % (c, "OK" if c in names else ("ALIAS->" + alias[c] if c in alias else "MISSING")))
