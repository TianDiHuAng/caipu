# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
d=json.load(io.open("data/ingredients.json",encoding="utf-8"))
idx={}
for it in d["items"]:
    idx[it["zh"]]=it["key"]
    for a in it.get("aliases",[]) or []:
        idx[a]=it["key"]
qs="鹅肉 土豆 粉条 黄豆酱 大葱 姜 大蒜 八角 干辣椒 生抽 老抽 料酒 盐 植物油 香菜 花椒 冰糖 桂皮 香叶 五花肉 血肠 干豆腐 黄瓜 米醋 辣椒油 白砂糖 香油 玉米面 面粉 酵母 酸菜 鸡蛋 玉米淀粉 小白菜 油菜 姜片 葱段 清水 陈醋 白糖 味精 鸡精 胡椒 白胡椒 蒜末 葱末".split()
print("未知:",[x for x in qs if x not in idx])
print("total",len(d["items"]))
