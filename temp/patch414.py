# -*- coding: utf-8 -*-
import json

p = "temp/drafts/batch-414.json"
D = json.load(open(p, encoding="utf-8"))
by = {r["id"]: r for r in D}

# 文本补长
T = {
 ("russian-stolichny-salad", "step", 5, "tip"): "翻拌的时候别用力压，土豆一压就散成泥，卖相全失。",
 ("russian-stolichny-salad", "step", 2, "tip"): "丁切得一样大，拌开后才好看，入口也均匀。",
 ("russian-stolichny-salad", "mistake", 1): "丁切得大大小小，端上桌卖相全无，口感也不齐。",
 ("russian-stolichny-salad", "mistake", 3): "用力压着拌，土豆全被压成泥浆，沙拉变糊。",
 ("russian-beet-walnut-salad", "step", 2, "tip"): "甜菜丝切太细会大量出水，粗丝才有嚼感。",
 ("russian-beet-walnut-salad", "step", 4, "tip"): "蒜泥一定要细，否则一口咬到会呛，破坏整体味。",
 ("russian-beet-walnut-salad", "step", 6, "tip"): "核桃最后撒，才能保持干脆的口感不被酱泡软。",
 ("russian-beet-walnut-salad", "mistake", 2): "甜菜丝切得极细，拌完出一碗红汤，口感也全无。",
 ("russian-cabbage-carrot-salad", "step", 0, "tip"): "丝切得越细，杀水越快，拌的时候也越入味。",
 ("russian-cabbage-carrot-salad", "step", 1, "tip"): "揉到菜丝软塌再停手，成品才脆爽而不生硬。",
 ("russian-cabbage-carrot-salad", "step", 3, "cue"): "碗里橙红与浅绿交错，丝条细匀",
 ("russian-cabbage-carrot-salad", "step", 5, "cue"): "菜丝油亮，颜色比拌之前更鲜",
 ("russian-cabbage-carrot-salad", "step", 6, "tip"): "冷藏半小时后菜丝更脆，酸味也变得柔和。",
 ("russian-egg-cheese-salad", "step", 0, "cue"): "蛋壳一敲就整片剥落，蛋白光洁",
 ("russian-egg-cheese-salad", "step", 4, "cue"): "蛋丁完整不散，酱色淡黄发亮",
 ("russian-omelet-milk", "step", 0, "tip"): "多搅半分钟让蛋液更匀，卷出来才够嫩滑。",
 ("russian-omelet-milk", "step", 5, "cue"): "两面金黄，按压能立刻回弹",
 ("russian-omelet-milk", "step", 6, "tip"): "出锅立刻切段，凉了会变挺，折起来容易裂。",
 ("russian-fried-eggs-tomato", "step", 1, "tip"): "黄油掺一点植物油一起用，煎的时候不容易焦。",
 ("russian-fried-eggs-tomato", "step", 5, "tip"): "盖盖小火焖，比大火直煎更容易控制熟度。",
 ("russian-fried-eggs-tomato", "step", 6, "tip"): "离火就上桌，蛋黄凉了会发硬，口感变差。",
 ("russian-fried-eggs-tomato", "mistake", 3): "大火煎到蛋黄全硬，吃起来像橡皮，毫无嫩感。",
 ("russian-fried-eggs-tomato", "variation", 0): "加两片煎过的酸黄瓜，酸味更开胃，也不腻口。",
 ("russian-stewed-cabbage", "step", 0, "tip"): "切粗丝炖完还有口感，切细丝会烂成一锅糊。",
 ("russian-stewed-cabbage", "step", 1, "tip"): "胡萝卜擦丝更容易炒出橙红色的油，颜色更漂亮。",
 ("russian-stewed-cabbage", "step", 3, "tip"): "先炒软再加盖炖，出来才不水汪汪，味也浓。",
 ("russian-stewed-cabbage", "step", 4, "tip"): "一点白醋能保住卷心菜的浅绿色，不发黄发暗。",
 ("russian-stewed-cabbage", "step", 5, "tip"): "中途翻两次就够，翻太勤菜丝会碎，卖相变差。",
 ("russian-stewed-cabbage", "step", 5, "cue"): "菜丝软透透明，锅底汤汁收薄",
 ("russian-stewed-cabbage", "tip", 2): "番茄先炒出汁再下菜，整锅的底味才够厚实。",
 ("russian-stewed-cabbage", "mistake", 2): "全程大火猛炖不转小火，锅底很快结一层焦。",
 ("russian-baked-beet", "step", 0, "tip"): "扎几个小孔能防止烤的时候表皮爆裂、汁水流光。",
 ("russian-baked-beet", "step", 1, "tip"): "刷一层油能让表皮烤得紧实，不会干裂开缝。",
 ("russian-baked-beet", "step", 3, "tip"): "趁温热剥皮最省力，凉透了皮会牢牢粘住肉。",
 ("russian-baked-beet", "step", 4, "tip"): "切厚一点吃着才有肉感，太薄容易碎在盘里。",
 ("russian-baked-beet", "step", 5, "tip"): "蒜末切得越细，酱才越顺滑，不会卡在嘴里。",
 ("russian-baked-beet", "step", 6, "tip"): "趁温热淋酱，酱会微微化开，更容易贴住切面。",
 ("russian-baked-beet", "mistake", 0): "削皮后裸烤，表面干硬开裂，里面却还是生的。",
}

for k, v in T.items():
    rid = k[0]
    r = by[rid]
    kind = k[1]
    if kind == "step":
        idx, field = k[2], k[3]
        r["steps"][idx][field] = v
    elif kind == "tip":
        r["tips"][k[2]] = v
    elif kind == "mistake":
        r["mistakes"][k[2]] = v
    elif kind == "variation":
        r["variations"][k[2]] = v

# 时长调整
FIX = {
 "russian-stolichny-salad": (20, 45),
 "russian-beet-walnut-salad": (20, 62),
 "russian-cabbage-carrot-salad": (55, 6),
 "russian-egg-cheese-salad": (25, 12),
 "russian-omelet-milk": (12, 10),
 "russian-fried-eggs-tomato": (8, 14),
 "russian-baked-beet": (12, 68),
}
for rid, (prep, cook) in FIX.items():
    by[rid]["prep"] = prep
    by[rid]["cook"] = cook

json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

bad = 0
for r in D:
    for i, s in enumerate(r["steps"]):
        for k, mk in (("t", 21), ("tip", 17), ("cue", 10)):
            if len(s[k]) < mk:
                bad += 1
                print("SHORT", r["id"], i, k, len(s[k]), s[k])
    for f, mk in (("tips", 17), ("mistakes", 17), ("variations", 17)):
        for t in r[f]:
            if len(t) < mk:
                bad += 1
                print("SHORT", r["id"], f, len(t), t)
    st = sum(s["time"] for s in r["steps"])
    if st > r["prep"] + r["cook"]:
        print("TIME", r["id"], st, r["prep"] + r["cook"])
print("bad", bad)
