# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-410.json")
D = json.load(io.open(p, encoding="utf-8"))

CUE = {
 ("kejia-xiami-men-doufu", 0): "虾米软胀，水色微黄发浑，闻着有海味",
 ("kejia-xiami-men-doufu", 1): "豆腐块完整，边缘不塌，切面平整",
 ("kejia-xiami-men-doufu", 4): "虾米卷曲发亮，香味扑鼻，油面泛起细泡",
 ("kejia-xiami-men-doufu", 5): "汤汁沸腾，香菇开始变软，浮起白沫",
 ("kejia-xiami-men-doufu", 7): "汤汁浓稠挂勺，蒜苗翠绿，锅边一圈亮油",
 ("kejia-fuzhu-men-rou", 0): "腐竹段软胀，弯折不发脆，捏着有韧劲",
 ("kejia-fuzhu-men-rou", 1): "肉块紧实，汤面浮沫撇净，水色转清",
 ("kejia-fuzhu-men-rou", 2): "肉块均匀裹上枣红色，锅底油亮发光",
 ("kejia-fuzhu-men-rou", 3): "酒气散尽，香气上来了，闻着没有腥味",
 ("kejia-fuzhu-men-rou", 4): "汤面微沸，肉块上色均匀，油花聚到锅边",
 ("kejia-fuzhu-men-rou", 5): "腐竹吸饱汤汁，颜色转深，压下去能回弹",
 ("kejia-fuzhu-men-rou", 6): "汤汁挂勺，油光发亮，锅底沙沙作响",
 ("kejia-luobo-paigu-tang", 0): "排骨发白，水色转淡红，血水泡出来",
 ("kejia-luobo-paigu-tang", 2): "排骨干净无沫，肉质不缩，表面发白",
 ("kejia-luobo-paigu-tang", 3): "汤色转白，排骨开始脱骨，肉轻推能动",
 ("kejia-luobo-paigu-tang", 6): "汤色清亮微白，咸淡合适，表面浮着油点",
 ("kejia-youyu-ganbei-tang", 0): "干贝软胀，撕开成丝状，中心不发硬",
 ("kejia-youyu-ganbei-tang", 1): "鱿鱼块带菱形花刀纹，纹路间距均匀",
 ("kejia-youyu-ganbei-tang", 2): "排骨干净，浮沫撇净，水色由浑转清",
 ("kejia-youyu-ganbei-tang", 3): "汤面浮起细密小泡，姜丝浮在上层",
 ("kejia-youyu-ganbei-tang", 4): "汤色浅黄清亮，干贝散开，油花细碎",
 ("kejia-youyu-ganbei-tang", 6): "鱿鱼卷起成筒，肉质发白，花刀撑开",
 ("kejia-youyu-ganbei-tang", 7): "汤清见底，葱花翠绿飘浮，碗边挂着油珠",
 ("kejia-dabaicai-xiancai", 0): "菜叶完整无泥，水面澄清，根部干净",
 ("kejia-dabaicai-xiancai", 1): "叶面干爽，边缘略有点软，摸上去不粘手",
 ("kejia-dabaicai-xiancai", 2): "菜帮薄片，菜叶宽条，分开盛放备用",
 ("kejia-dabaicai-xiancai", 3): "菜叶发软，盆底积出盐水，手捏能出水",
 ("kejia-dabaicai-xiancai", 5): "配料拌匀，红糖颗粒分散，辣椒圈均匀",
 ("kejia-dabaicai-xiancai", 6): "菜层紧实，卤汁升到菜面，看不到空隙",
 ("kejia-dabaicai-xiancai", 7): "缸口封严，卤汁清亮微浑，重石压得稳",
 ("kejia-luobogan", 0): "萝卜表皮光洁，须根去净，没有黑心",
 ("kejia-luobogan", 4): "表面干爽，手捏不粘，条身微微发韧",
 ("kejia-luobogan", 5): "配料裹匀，红糖颗粒化开，辣圈分布均匀",
 ("kejia-luobogan", 7): "罐口封严，卤汁微浑清亮，重石压住不浮",
 ("kejia-xiami-zhengdan", 0): "虾米软胀，碎末均匀，没有硬芯",
 ("kejia-xiami-zhengdan", 1): "蛋液均匀无絮状蛋白，颜色一致",
 ("kejia-xiami-zhengdan", 3): "蛋液澄清细腻，筛上留渣，气泡消失",
 ("kejia-xiami-zhengdan", 4): "表面无泡，蛋液平整，浮沫撇得干净",
 ("kejia-xiami-zhengdan", 5): "碗口封严，膜上有小孔，边缘贴紧碗壁",
 ("kejia-xiami-zhengdan", 7): "蛋面如镜，葱花翠绿点缀，边缘不塌",
 ("kejia-dougan-chao-qincai", 0): "豆干条整齐，断面平整，长短基本一致",
 ("kejia-dougan-chao-qincai", 1): "芹菜段翠绿，粗筋已撕净，切面水亮",
 ("kejia-dougan-chao-qincai", 2): "芹菜段翠绿透亮，摸着脆，水汽已控干",
 ("kejia-dougan-chao-qincai", 3): "豆干条表面微黄起皱，边缘略卷",
 ("kejia-dougan-chao-qincai", 4): "蒜片微黄，辣香冲鼻，油色微红",
 ("kejia-dougan-chao-qincai", 6): "芹菜翠绿挺直，豆干油亮，翻动有脆响",
}

TIP = {
 ("kejia-fuzhu-men-rou", 7): "蒜苗断生就起锅，久炒发黄，辛香也全跑光了。",
 ("kejia-luobo-paigu-tang", 0): "泡水能去掉大部分血水，汤才会清亮不腥，比焯水更关键。",
 ("kejia-youyu-ganbei-tang", 7): "鱿鱼本身带咸味，盐要少放，先尝一口再决定补不补。",
 ("kejia-luobogan", 6): "罐子必须彻底干透，带一点生水整罐都会坏掉。",
}

TEXT = {
 ("kejia-luobo-paigu-tang", 7): "关火后撒白胡椒和葱花，盛进汤碗上桌，趁热喝最暖胃，凉了腥味就出来。",
 ("kejia-youyu-ganbei-tang", 7): "加盐和白胡椒调味，淋几滴香油，撒葱花盛碗，趁热喝汤最鲜。",
}

# 主料调整：虾米/干贝移至 aux
MOVE = {"kejia-xiami-men-doufu": ["虾米"], "kejia-youyu-ganbei-tang": ["干贝"], "kejia-xiami-zhengdan": ["虾米"]}

for r in D:
    r["overwrite"] = True
    for i, s in enumerate(r["steps"]):
        k = (r["id"], i)
        if k in CUE:
            s["cue"] = CUE[k]
        if k in TIP:
            s["tip"] = TIP[k]
        if k in TEXT:
            s["t"] = TEXT[k]
    if r["id"] in MOVE:
        moved = []
        for g in r["ingredients"]:
            if g["group"] == "main":
                keep = []
                for it in g["items"]:
                    (moved if it["n"] in MOVE[r["id"]] else keep).append(it)
                g["items"] = keep
        for g in r["ingredients"]:
            if g["group"] == "aux":
                g["items"] = moved + g["items"]

json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("patched", len(D))
