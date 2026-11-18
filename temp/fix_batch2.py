# -*- coding: utf-8 -*-
import json, io, os
base = r"D:\AI\project\marvis_project\caipu\data\recipes"

def load(rel):
    p = os.path.join(base, rel)
    return p, json.loads(open(p, encoding="utf-8-sig").read())

def save(p, r):
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

fixes = []

# jingjiang-rousi
p, r = load(r"cn\beijing\jingjiang-rousi.json")
for s in r["steps"]:
    s["text"] = s["text"].replace("碎成肉末", "碎成小粒")
    s["tip"] = s["tip"].replace("碎成肉末", "碎成小粒")
r["steps"][-1]["text"] = r["steps"][-1]["text"].replace(
    "肉丝表面油亮、酱色均匀，盘底几乎不见流动的汤汁，葱丝仍挺立。",
    "肉丝表面油亮、酱色均匀，盘底几乎不见流动的汤汁，葱丝仍挺立。")
# 在倒数第二步（滑肉丝后炒酱）后补一句豆腐皮处理，用一个步骤承载
r["steps"][2]["text"] = ("豆腐皮切成 12 厘米见方的片，放入沸水中烫 10 秒去掉豆腥味，捞出沥干后叠放摆盘；"
                         "甜面酱 50 克加 20 克白糖与 40 毫升清水调开，另取 5 克玉米淀粉加 15 毫升清水调成水淀粉备用。")
fixes.append(r["id"])
save(p, r)

# chizhi-paigu
p, r = load(r"cn\cantonese\chizhi-paigu.json")
for grp in r["ingredients"]:
    for it in grp["items"]:
        if it["name"] == "大葱":
            it["name"] = "小葱"
            it["name_en"] = "scallion"
r["steps"][-1]["text"] = "关火后焖 2 分钟再开盖，撒上小葱切成的葱末即可上桌。"
for s in r["steps"]:
    s["tip"] = s["tip"].replace("晾凉再腌肉", "晾凉后再拌入排骨")
fixes.append(r["id"])
save(p, r)

# lawi-hezheng
p, r = load(r"cn\hunan\lawi-hezheng.json")
r["steps"][0]["text"] = ("腊肉用温水加少许食用碱面刷洗表面烟熏层，再用清水冲净；"
                         "整块冷水下锅煮 8 分钟，去除多余盐分与表面油污。")
r["steps"][-1]["text"] = "出锅后淋 5 毫升香油，撒少许大葱切成的葱末，趁热连同汤汁一起上桌。"
fixes.append(r["id"])
save(p, r)

# shizitou
p, r = load(r"cn\jiangsu\shizitou.json")
for s in r["steps"]:
    s["text"] = s["text"].replace("肉馅", "肉料")
    s["tip"] = s["tip"].replace("肉馅", "肉料")
fixes.append(r["id"])
save(p, r)

# xihu-cuyu
p, r = load(r"cn\zhejiang\xihu-cuyu.json")
for s in r["steps"]:
    s["visual_cue"] = s["visual_cue"].replace("蒜瓣状", "片状")
fixes.append(r["id"])
save(p, r)

# shuizhu-niurou
p, r = load(r"cn\sichuan\shuizhu-niurou.json")
r["tips"] = [t.replace("牛肉久煮必老", "牛里脊久煮必老").replace("牛肉选里脊或黄瓜条", "牛里脊选里脊中段或黄瓜条部位")
             for t in r["tips"]]
r["diet_tags"] = [d for d in r["diet_tags"] if d != "gluten-free"]
fixes.append(r["id"])
save(p, r)

# congsao-haishen
p, r = load(r"cn\shandong\congsao-haishen.json")
r["diet_tags"] = [d for d in r["diet_tags"] if d != "gluten-free"]
fixes.append(r["id"])
save(p, r)

# ziran-yangrouchuan
p, r = load(r"cn\xinjiang\ziran-yangrouchuan.json")
r["steps"][2]["time_min"] = 0
r["diet_tags"] = [d for d in r["diet_tags"] if d != "gluten-free"]
fixes.append(r["id"])
save(p, r)

print("touched:", fixes)
