# -*- coding: utf-8 -*-
import json, io, os, glob
T = r"E:\ai_project\marvis_project\caipu"
tax = json.load(io.open(T + r"\data\taxonomy.json", encoding="utf-8"))
cu = [c for c in tax["cuisines"] if c["slug"] == "yunguai"][0]
print("cats", cu.get("categories"), "unsupported", cu.get("unsupported"))
cat = {c["slug"]: c.get("name") for c in tax["categories"]}
print({k: cat.get(k) for k in cu.get("categories", [])})
ids = []
for f in glob.glob(T + r"\data\recipes\cn\yunguai\*.json"):
    d = json.load(io.open(f, encoding="utf-8"))
    ids.append((d["id"], d["category"] if isinstance(d["category"], str) else d["category"], d["title"] if "title" in d else d.get("name", {})))
print(len(ids))
for x in sorted(ids, key=lambda y: str(y[1])): print(x)
ing = json.load(io.open(T + r"\data\ingredients.json", encoding="utf-8"))["items"]
want = ["折耳根", "鱼腥草", "小米椒", "酸汤", "木姜子", "腊肉", "土豆", "苦菜", "酸菜", "豆豉", "糟辣椒", "牛肝菌", "干巴菌", "鸡枞", "米线", "饵块", "火腿", "酱油", "糯米", "小米", "玉米", "芭蕉叶", "香茅", "柠檬", "芫荽", "薄荷", "紫苏", "酸豆", "酸笋", "魔芋", "蕨菜", "竹笋", "香菇", "五花肉", "排骨", "牛肉", "鸡腿肉", "猪里脊", "蒜苗", "干辣椒", "花椒", "料酒", "米酒", "蚝油", "生抽", "老抽", "白糖", "盐", "植物油", "猪油", "香油", "白胡椒", "玉米淀粉", "鸡蛋", "豆腐", "嫩豆腐", "葱", "小葱", "大蒜", "姜", "清水"]
names = set()
for it in ing:
    names.add(it["zh"])
    for a in it.get("aliases", []): names.add(a)
for w in want:
    print(w, "OK" if w in names else "MISS")
