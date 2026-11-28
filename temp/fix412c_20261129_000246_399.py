# -*- coding: utf-8 -*-
import json
p = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\thai\thai-tao-hu-neung.json"
d = json.load(open(p, encoding="utf-8"))
d["name"]["zh"] = "泰式姜香蒸豆腐"
for g in d["ingredients"]:
    for it in g["items"]:
        if it["name"] == "南姜":
            it["name"] = "姜"
            it["note"] = "切细末"
for s in d["steps"]:
    s["text"] = s["text"].replace("南姜", "姜")
d["tips"] = [t.replace("南姜", "姜") for t in d["tips"]]
d["origin_note"] = d["origin_note"].replace("南南姜香", "姜香").replace("南姜", "姜")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(d["origin_note"])
print([i["name"] for g in d["ingredients"] for i in g["items"]])
