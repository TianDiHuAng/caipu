# -*- coding: utf-8 -*-
import json, io
ing = json.load(io.open(r"E:\ai_project\marvis_project\caipu\data\ingredients.json", encoding="utf-8"))["items"]
names = {}
for it in ing:
    names[it["zh"]] = it["id"]
    for a in it.get("aliases", []):
        names.setdefault(a, it["id"])
want = ["芥菜", "萝卜", "白萝卜", "豆干", "豆腐干", "腐竹", "猪大肠", "鱿鱼", "南乳", "黄酒", "糯米", "芋头",
        "面筋", "大白菜", "咸菜", "萝卜干", "豆角", "香菇", "五花肉", "猪肉", "排骨", "鸡腿肉", "鸡蛋",
        "酸菜", "梅干菜", "豆豉", "腐乳", "蒜苗", "小米椒", "干辣椒", "白胡椒", "玉米淀粉", "淀粉",
        "虾米", "木耳", "笋干", "冬笋", "竹笋", "米酒", "红糖", "冰糖", "鹌鹑蛋", "枸杞", "香醋", "陈醋",
        "八角", "桂皮", "香叶", "芹菜", "葱花", "红曲米", "蒜蓉", "朝天椒", "豆腐皮", "油豆腐", "豆泡",
        "肉馅", "鲮鱼", "草鱼", "鲫鱼", "腊肠", "香肠", "腊肉", "蚝豉", "干贝", "瑶柱", "香菇干", "蒜头"]
miss = [w for w in want if w not in names]
print("MISS:", miss)
for w in want:
    if w in names: print(w, names[w])
