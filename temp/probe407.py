# -*- coding: utf-8 -*-
import json, io, os, glob
root = r"E:\ai_project\marvis_project\caipu"
tax = json.load(io.open(os.path.join(root, "data", "taxonomy.json"), encoding="utf-8"))
cu = {c["slug"]: c for c in tax["cuisines"]}["hongkong"]
lines = ["hk categories: " + str(cu.get("categories"))]
lines.append("unsupported: " + str(cu.get("unsupported")))
prog = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
def walk(node):
    if isinstance(node, dict):
        if node.get("slug") == "hongkong" and "cells" in str(list(node.keys())):
            lines.append("hk node: " + json.dumps(node, ensure_ascii=False)[:1500])
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)
walk(prog["regions"])
files = sorted(glob.glob(os.path.join(root, "data", "recipes", "cn", "hongkong", "*.json")))
ids = [os.path.basename(f)[:-5] for f in files]
lines.append("hk ids(%d): %s" % (len(ids), ", ".join(ids)))
ing = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
want = ["虾", "蟹", "蚝", "鲍", "花胶", "瑶柱", "干贝", "肠粉", "米粉", "河粉", "面", "陈皮", "柱侯", "腐乳", "南乳", "豉油", "生抽", "老抽", "蚝油", "叉烧", "烧鹅", "腊肠", "腊肉", "白粥", "皮蛋", "咸蛋", "腐竹", "白果", "绿豆", "红豆", "椰浆", "淡奶", "炼乳", "菠萝", "猪手", "牛腩", "排骨", "鸡翅", "鲮鱼", "鱼滑", "墨鱼", "扇贝", "豆豉", "沙姜", "葱", "姜", "蒜"]
hit = {}
for w in want:
    names = [it["zh"] for it in ing if w in it["zh"] or any(w in a for a in it.get("aliases", []))]
    hit[w] = names[:4]
lines.append(json.dumps(hit, ensure_ascii=False))
io.open(os.path.join(root, "temp", "hk_probe.txt"), "w", encoding="utf-8").write("\n".join(lines))
