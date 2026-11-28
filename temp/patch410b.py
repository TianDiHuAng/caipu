# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-410.json")
D = json.load(io.open(p, encoding="utf-8"))

for r in D:
    r["overwrite"] = True
    if r["id"] == "kejia-dabaicai-xiancai":
        r["servings"] = 12
        r["prep"] = 180
        r["cook"] = 10
        r["steps"][0]["time"] = 15
        r["nutrition"] = dict(basis="按十二人份估算", kcal=45, protein=2, fat=0.7, carbs=8, sodium=990)
    if r["id"] == "kejia-luobogan":
        r["prep"] = 620
        r["cook"] = 15
        r["nutrition"] = dict(basis="按十人份估算", kcal=52, protein=2, fat=0.4, carbs=11, sodium=1320)
    if r["id"] == "kejia-luobo-paigu-tang":
        for s in r["steps"]:
            s["t"] = s["t"].replace("排骨的蛋白质凝固", "排骨的肉纤维收紧").replace("蛋白质凝固", "肉纤维收紧")
            s["tip"] = s["tip"].replace("蛋白质凝固", "肉纤维收紧")
    if r["id"] == "kejia-youyu-ganbei-tang":
        r["diet"] = [d for d in r["diet"] if d != "pescatarian"]

json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("patched2")
