# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p = "temp/drafts/batch-308.json"
data = json.load(open(p, encoding="utf-8"))
for r in data:
    rid = r["id"]
    if rid == "shandong-ban-sansi":
        r["steps"][4]["t"] = "白菜丝、粉丝段、胡萝卜丝放进拌菜盆，加蒜末、香醋、生抽、盐、白糖和芝麻油抓拌。"
    if rid == "shandong-hongshao-doufu":
        r["safety"] = ["香菇须彻底加热炒透，避免半生带出生菌味。",
                       "煎豆腐时油量较多，豆腐片须吸干水分再下锅，防止热油飞溅。"]
    if rid == "shandong-huasheng-bocai":
        r["diet"] = ["vegetarian", "vegan", "dairy-free", "low-carb"]
    if rid == "shandong-jidan-geng":
        r["diet"] = ["high-protein", "dairy-free", "low-carb"]
        r["related"] = ["shandong-suanla-tang", "shandong-zicai-danhua-tang"]
    if rid == "shandong-zicai-danhua-tang":
        r["safety"] = ["蛋液须在汤中彻底加热至完全凝固，不可留生蛋液。",
                       "紫菜须冲洗去除泥沙，散装紫菜建议先过一遍清水再使用。"]
    if rid == "shandong-xianggu-men-ji":
        r["related"] = ["shandong-xianggu-shao-doufu", "shandong-hongshao-doufu"]
    r["overwrite"] = True
json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
