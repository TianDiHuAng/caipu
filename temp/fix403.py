# -*- coding: utf-8 -*-
import json
b = r"E:\ai_project\marvis_project\caipu\data\recipes\cn\jiangsu" + "\\"
def L(i): return json.load(open(b + i + ".json", encoding="utf-8"))
def W(i, d): json.dump(d, open(b + i + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

d = L("jiangsu-youshen-jiaobai")
d["steps"][5]["text"] = "淋一圈芝麻油，撒上葱花，快速翻两下即可出锅装盘。"
d["common_mistakes"][0] = "茭白没去掉底部老根，吃起来一口渣，白费了好料。"
W("jiangsu-youshen-jiaobai", d)

d = L("jiangsu-babao-fan")
d["steps"][5]["text"] = "上蒸锅大火蒸四十分钟，倒扣在盘里脱模，用玉米淀粉勾薄芡淋上即可。"
for it in d["ingredients"]:
    for x in it["items"]:
        if x["name"] == "清水":
            x["note"] = "蒸锅用水"
d["steps"][1]["text"] = "泡好的糯米沥干，上蒸锅大火蒸三十分钟，蒸锅里的清水要一次加足。"
W("jiangsu-babao-fan", d)

d = L("jiangsu-gan-shao-guiyu")
d["diet_tags"] = []
W("jiangsu-gan-shao-guiyu", d)

d = L("jiangsu-pipa-doufu")
d["steps"][1]["text"] = "虾仁剔掉背上的黑线剁成细茸，加绍兴酒、盐与白胡椒粉搅到发黏。"
W("jiangsu-pipa-doufu", d)
print("ok")
