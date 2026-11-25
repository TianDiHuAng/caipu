# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
items = json.load(open("data/ingredients.json", encoding="utf-8"))["items"]
names = set(i["zh"] for i in items)
alias = {}
for it in items:
    for a in it.get("aliases", []):
        alias.setdefault(a, it["zh"])
check = ["鹰嘴豆", "菠菜", "茄子", "嫩豆腐", "北豆腐", "鸡蛋", "生菜", "番茄", "黄瓜", "洋葱",
         "扁豆", "绿扁豆", "橄榄油", "红椒粉", "烟熏红椒粉", "藏红花", "大蒜", "面包", "土豆",
         "红豆", "白豆", "青椒", "柠檬", "欧芹", "香菜", "猪肉末", "香肠", "米饭", "鸡汤",
         "白葡萄酒", "红葡萄酒醋", "雪莉醋", "黑胡椒", "海盐", "西红柿", "甜椒"]
for c in check:
    print("%-10s %s" % (c, "OK" if c in names else ("ALIAS->" + alias[c] if c in alias else "MISSING")))
tax = json.load(open("data/taxonomy.json", encoding="utf-8"))
for cu in tax["cuisines"]:
    if cu["slug"] == "spanish":
        print("categories:", [c["slug"] if isinstance(c, dict) else c for c in cu.get("categories", [])])
        print("unsupported:", cu.get("unsupported"))
print("all cats:", [c["slug"] for c in tax["categories"]])
