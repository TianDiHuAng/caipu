# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
def load(n):
    path = os.path.join(root, "data", "recipes", "intl", "korean", n + ".json")
    return path, json.load(io.open(path, encoding="utf-8"))
def save(path, d):
    json.dump(d, io.open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 1 buchu: 红椒 -> 小米辣
path, d = load("korean-buchu-muchim")
for s in d["steps"]:
    s["visual_cue"] = s["visual_cue"].replace("红椒圈", "小米辣圈")
save(path, d)

# 2 gamja: 辣椒粉未使用 -> 在后两步加入
path, d = load("korean-gamja-jorim")
for s in d["steps"]:
    if s["n"] == 5:
        s["text"] = "倒入浓口酱油和白糖翻匀，再撒辣椒粉，让每块土豆都裹上酱色。"
    if s["n"] == 8:
        s["text"] = "淋香油、撒辣椒粉和芝麻葱花，装盘时把酱汁浇在上面，热吃最香。"
save(path, d)

# 3 bokkeum: 奶油/吐司
path, d = load("korean-gyeran-bokkeum")
for s in d["steps"]:
    s["text"] = s["text"].replace("奶油般的质地", "绵密如脂的质地").replace("配吐司或白饭都很合适", "配米饭或馒头都很合适").replace("配吐司或白饭都合适", "配米饭都合适")
    s["tip"] = s["tip"].replace("奶油般的质地", "绵密如脂的质地")
d["serving_suggestion"] = d["serving_suggestion"].replace("配吐司或白饭都适合", "配白饭或热馒头都适合")
d["variations"] = [v.replace("配吐司或白饭都合适", "配白饭都合适").replace("铺在白饭上", "铺在白饭上") for v in d["variations"]]
save(path, d)

# 4 kimchi mari: 芝麻未使用
path, d = load("korean-kimchi-gyeran-mari")
for s in d["steps"]:
    if s["n"] == 8:
        s["text"] = "卷好的蛋卷留在锅里小火定型一分钟，出锅稍凉后切厚片，撒上芝麻装盘。"
save(path, d)
print("done")
