# -*- coding: utf-8 -*-
import json, io
p = r"E:\ai_project\marvis_project\caipu\temp\drafts\batch-408.json"
D = json.load(io.open(p, encoding="utf-8"))
byid = {r["id"]: r for r in D}

# 1 蚝油含水产，取消素食标记
byid["hongkong-haoyou-jielan"]["diet"] = ["dairy-free"]
byid["hongkong-hongshao-doufu-bao"]["diet"] = ["dairy-free"]

# 2 咸蛋蒸肉饼饭：香油需在步骤中使用
r = byid["hongkong-xiandan-roubing-fan"]
r["steps"][7]["t"] = "取出后撒葱花，淋上香油，把肉饼和盘底的汁水一起铺在饭上即可。"
r["steps"][7]["cue"] = "肉汁渗进饭里，表面油润发亮"

# 3 咸鱼鸡粒炒饭：避免出现未配料的鸡胸肉表述
r2 = byid["hongkong-xianyu-jili-chaofan"]
r2["tips"][2] = "鸡肉要用鸡腿肉切粒，腿肉带一点油脂，炒久了也不柴，比纯瘦的部位嫩得多。"

json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixed")
