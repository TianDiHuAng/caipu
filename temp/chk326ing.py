# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
d=json.load(io.open("data/ingredients.json",encoding="utf-8"))
items=d["items"] if isinstance(d,dict) else d
idx={}
for it in items:
    if not isinstance(it,dict): continue
    for k in ("zh","en","id"):
        if it.get(k): idx[str(it[k])]=it.get("zh") or it.get("id")
    for a in it.get("aliases",[]) or []:
        idx[a]=it.get("zh") or it.get("id")
q="鹅 鹅肉 大鹅 血肠 猪血 干豆腐 豆腐皮 玉米面 玉米面粉 酸菜 粉条 粉丝 五花肉 猪肉 豆角 排骨 土豆 大葱 生姜 大蒜 八角 花椒 桂皮 香叶 干辣椒 生抽 老抽 料酒 盐 白砂糖 冰糖 植物油 花生油 面粉 鸡蛋 淀粉 玉米淀粉 香菜 青椒 红椒 木耳 白萝卜 白菜 辣椒面 孜然 米醋 陈醋 黄豆酱 甜面酱 蚝油 鸡精 味精 高汤 清汤 葱 姜 蒜 蒜末 姜片 花椒粉 胡椒粉 碱面 白面 荞麦面 小米 大黄米 红豆 糯玉米 猪蹄 猪骨 猪皮".split()
unk=[x for x in q if x not in idx]
print("未知:",unk)
print("总数",len(items))
for x in ["酸菜","粉条","五花肉","干豆腐","玉米面","鹅肉","猪血","大葱","生姜","大蒜","植物油","面粉","淀粉","冰糖","黄豆酱","米醋","白胡椒粉","胡椒粉","粉丝","土豆","豆角"]:
    print(x,"->",idx.get(x))
