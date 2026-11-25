# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p = "temp/drafts/batch-307.json"
data = json.load(open(p, encoding="utf-8"))

steps_tip = {
 ("shandong-chao-hecai",5): "韭黄最后下锅，多炒十秒就会发黄发软。",
 ("shandong-liangban-haidaisi",2): "焯完马上过一遍凉水，海带丝才脆得住。",
 ("shandong-niang-doufu",0): "豆腐表面吸得越干，煎的时候就越不容易粘锅。",
 ("shandong-niang-doufu",1): "始终顺同一个方向搅，肉馅才抱团不出水。",
 ("shandong-niang-doufu",3): "坑里撒的那层淀粉是粘合剂，煎的时候肉馅才不会掉。",
 ("shandong-niang-doufu",4): "先煎有肉的一面再煎豆腐面，肉馅才不容易散。",
 ("shandong-niang-doufu",5): "芡一定要薄，能挂住豆腐表面就够，厚了整盘发糊。",
 ("shandong-qincai-chaorousi",1): "上浆时抓进一点清水，肉丝炒出来才够嫩。",
 ("shandong-qincai-chaorousi",3): "滑肉丝的油温别太高，六成热下锅最嫩。",
 ("shandong-qincai-chaorousi",5): "盐一定要最后放，放早了芹菜会出水变软。",
 ("shandong-ruanzha-liji",0): "逆着肉的纹理下刀，炸出来才不塞牙。",
 ("shandong-ruanzha-liji",3): "椒盐要现炒现擀，放久了只剩下咸味。",
 ("shandong-ruanzha-liji",4): "一根根分开下锅，粘成一坨就不好分开。",
 ("shandong-ruanzha-liji",5): "复炸只求外壳脆，时间一长肉就柴了。",
 ("shandong-shao-qiezi",1): "粉层能挡住油，茄子就不会变成油包。",
 ("shandong-shao-qiezi",3): "汤汁烧开后再下茄子，味道才挂得均匀。",
 ("shandong-shao-qiezi",4): "用勺背推着翻，别用勺沿铲，茄子容易碎。",
 ("shandong-shao-qiezi",5): "醋沿着热锅边淋下去，酸香才冲得出来。",
}
steps_t = {
 ("shandong-qincai-chaorousi",5): "倒回滑好的肉丝，加生抽和盐快速翻匀，出锅装盘。",
}
steps_cue = {
 ("shandong-shao-qiezi",3): "汤汁酱红油亮，蒜香四溢",
}
tips = {
 ("shandong-shao-qiezi",1): "茄子腌过再炸，既省油，炸完也不易回软。",
}
mises = {
 ("shandong-liangban-haidaisi",0): "海带泡得不够久，咬着发硬还带一股沙感。",
 ("shandong-qincai-chaorousi",1): "肉丝不上浆直接下锅炒，出锅又干又柴。",
}
vars_ = {
 ("shandong-ruanzha-liji",0): "面糊里加十克炒熟的芝麻，外壳更香更脆。",
 ("shandong-shao-qiezi",0): "加五十克切薄的猪肉片同烧，荤香更足。",
}
prep = {
 "shandong-liangban-haidaisi": 24,
 "shandong-ruanzha-liji": 27,
}

for r in data:
    rid = r["id"]
    for i, s in enumerate(r["steps"]):
        if (rid, i) in steps_tip: s["tip"] = steps_tip[(rid, i)]
        if (rid, i) in steps_t: s["t"] = steps_t[(rid, i)]
        if (rid, i) in steps_cue: s["cue"] = steps_cue[(rid, i)]
    for i in range(len(r["tips"])):
        if (rid, i) in tips: r["tips"][i] = tips[(rid, i)]
    for i in range(len(r["mistakes"])):
        if (rid, i) in mises: r["mistakes"][i] = mises[(rid, i)]
    for i in range(len(r["variations"])):
        if (rid, i) in vars_: r["variations"][i] = vars_[(rid, i)]
    if rid in prep: r["prep"] = prep[rid]

json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("patched", len(data))
