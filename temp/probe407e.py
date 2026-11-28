# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
ing = json.load(io.open(os.path.join(root, "data", "ingredients.json"), encoding="utf-8"))["items"]
want = ["淀粉", "生粉", "白胡椒", "白砂糖", "生抽", "老抽", "香油", "植物油", "米酒", "冰糖", "清水",
        "青豆", "玉米", "马蹄", "豆豉", "虾", "芥蓝", "嫩豆腐", "大米", "鸡腿肉"]
out = {}
for w in want:
    out[w] = sorted({it["zh"] for it in ing if w in it["zh"] or any(w in a for a in it.get("aliases", []))})[:6]
io.open(os.path.join(root, "temp", "hk_probe3.json"), "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1))
