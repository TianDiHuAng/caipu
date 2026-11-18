# -*- coding: utf-8 -*-
import json, os
base = r"D:\AI\project\marvis_project\caipu\data\recipes"

def load(rel):
    p = os.path.join(base, rel)
    return p, json.loads(open(p, encoding="utf-8-sig").read())

def save(p, r):
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

p, r = load(r"cn\jiangsu\shizitou.json")
for s in r["steps"]:
    s["visual_cue"] = s["visual_cue"].replace("肉馅", "肉料")
    s["text"] = s["text"].replace("肉馅", "肉料")
    s["tip"] = s["tip"].replace("肉馅", "肉料")
save(p, r)

p, r = load(r"cn\sichuan\shuizhu-niurou.json")
for s in r["steps"]:
    s["tip"] = s["tip"].replace("牛肉久煮必老", "牛里脊久煮必老")
    s["text"] = s["text"].replace("牛肉久煮必老", "牛里脊久煮必老")
    s["visual_cue"] = s["visual_cue"].replace("牛肉久煮必老", "牛里脊久煮必老")
save(p, r)
print("ok")
