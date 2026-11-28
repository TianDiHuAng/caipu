# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
ing = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
want = ["芥兰", "空心菜", "通菜", "扇贝", "带子", "咸鱼", "鲈鱼", "豆腐", "腐乳", "蚝油", "菜心", "生菜",
        "香菇", "北菇", "红茶", "淡奶", "炼乳", "咸柠檬", "猪肉末", "鸡肉", "鸡蛋", "咸蛋", "糯米", "米",
        "腊肠", "叉烧", "虾仁", "虾米", "姜", "葱", "蒜", "红葱头", "陈皮", "豆豉", "黄豆", "鸡腿",
        "猪里脊", "五花肉", "青椒", "胡萝卜", "baking", "面粉", "澄粉", "猪油", "牛油"]
out = {}
for w in want:
    names = []
    for it in ing:
        if w in it["zh"] or any(w in a for a in it.get("aliases", [])):
            names.append(it["zh"])
    out[w] = sorted(set(names))[:6]
io.open(os.path.join(root, "temp", "hk_probe2.json"), "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=True, indent=1))
