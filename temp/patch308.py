# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p = "temp/drafts/batch-308.json"
data = json.load(open(p, encoding="utf-8"))

steps_tip = {
 ("shandong-ban-sansi",3): "胡萝卜焯一下能去生味，颜色也更亮更好看。",
 ("shandong-zicai-danhua-tang",2): "豆腐先煮一会儿再下蛋液，汤才清而有味。",
 ("shandong-zicai-danhua-tang",4): "紫菜一定要最后放，久煮就会发黏发暗。",
 ("shandong-huasheng-bocai",3): "水里滴几滴油，菠菜焯完颜色才翠绿好看。",
 ("shandong-huasheng-bocai",5): "花生米必须最后放，拌早了吸潮就软了。",
 ("shandong-hongshao-doufu",5): "青椒最后下锅，断生就起，脆绿才好看。",
 ("shandong-xianggu-men-ji",4): "水要一次加够，中途添水会把味道冲淡了。",
 ("shandong-xianggu-men-ji",5): "收汁的时候多晃几下锅，糖分很容易糊底。",
}
mises = {
 ("shandong-jidan-geng",1): "蛋液没有过筛就上锅，蒸好碗底沉了一层白絮。",
 ("shandong-hongshao-doufu",2): "老抽放得太多，成菜发黑发苦，卖相全毁了。",
 ("shandong-xianggu-men-ji",1): "糖色炒过头了，整锅都带苦味，颜色也发黑。",
}
vars_ = {
 ("shandong-zicai-danhua-tang",1): "出锅前撒一把香菜段，清香味更足更好闻。",
}
prep = {
 "shandong-ban-sansi": 25,
 "shandong-huasheng-bocai": 16,
 "shandong-hongshao-doufu": 17,
 "shandong-xianggu-men-ji": 25,
}

for r in data:
    rid = r["id"]
    for i, s in enumerate(r["steps"]):
        if (rid, i) in steps_tip: s["tip"] = steps_tip[(rid, i)]
    for i in range(len(r["mistakes"])):
        if (rid, i) in mises: r["mistakes"][i] = mises[(rid, i)]
    for i in range(len(r["variations"])):
        if (rid, i) in vars_: r["variations"][i] = vars_[(rid, i)]
    if rid in prep: r["prep"] = prep[rid]

json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("patched")
