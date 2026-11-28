# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-409.json")
D = json.load(io.open(p, encoding="utf-8"))
for r in D:
    r["overwrite"] = True
    # 1 淀粉 → 表面浆水
    if r["id"] == "guizhou-ganjiao-tudoupian":
        for s in r["steps"]:
            s["t"] = s["t"].replace("洗掉表面淀粉", "洗掉表面的白色浆水")
            s["tip"] = s["tip"].replace("淀粉洗得越干净", "白色浆水洗得越干净")
        r["tips"] = [x.replace("淀粉", "白色浆水").replace("表面的白色浆水洗得越干净", "白色浆水洗得越干净") for x in r["tips"]]
        r["mistakes"] = [x.replace("淀粉", "白色浆水") for x in r["mistakes"]]
    # 2 回锅肉加盐
    if r["id"] == "guizhou-huiguo-rou":
        for s in r["steps"]:
            s["t"] = s["t"].replace("加白糖翻匀，让每片肉都裹上酱色", "加白糖和盐翻匀，让每片肉都裹上酱色")
            s["tip"] = s["tip"].replace("老抽只上色，两三毫升就够", "老抽只上色，两三毫升就够，盐要在这一步补进去")
    # 3 牛肉：蛋白质 → 肉的纤维
    if r["id"] == "yunnan-xiaomila-chao-niurou":
        for s in r["steps"]:
            s["t"] = s["t"].replace("蛋白质上劲了", "肉的纤维上劲了")
            s["tip"] = s["tip"].replace("抓到发黏说明蛋白质上劲了", "抓到发黏说明肉纤维已经上劲")
        r["tips"] = [x.replace("蛋白质", "肉纤维") for x in r["tips"]]
        r["mistakes"] = [x.replace("蛋白质", "肉纤维") for x in r["mistakes"]]
    # 4 related 修正
    r["related"] = ["yunnan-suancai-chao-yumi" if x == "yunnan-suancai-chaoyumi" else x for x in r.get("related", [])]
json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixed")
for r in D:
    if r["id"] in ("guizhou-ganjiao-tudoupian", "yunnan-xiaomila-chao-niurou", "guizhou-huiguo-rou"):
        print(r["id"], r.get("related"))
