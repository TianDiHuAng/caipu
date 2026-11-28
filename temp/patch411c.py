# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-411.json")
D = json.load(io.open(p, encoding="utf-8"))

TIPS = {
 "表面带水下油锅会爆油，容易烫手。": "土豆表面带水下油锅会剧烈爆油，很容易烫到手，必须擦干。",
 "香油关火后再淋，香气才留得住。": "香油一定要关火之后再淋，高温会把香油的香气全部挥发掉。",
 "带水的韭菜拌好会出水，味道变淡。": "带水的韭菜拌好以后会不断出水，味道被稀释得又淡又水。",
 "鱼露带咸鲜，盐要少放，尝过再补。": "鱼露本身带着咸鲜，盐要少放，拌匀后尝一口再决定补多少。",
 "酱油沿碗边淋一圈，颜色均匀不砸坑。": "酱油要沿着碗边慢慢淋一圈，颜色分布均匀也不会砸出坑。",
}
CUES = {"蔬菜丝均匀裹上蛋液": "蔬菜丝均匀裹上蛋液，颜色分明"}
TEXTS = {"淋两滴香油，装盘趁热吃，配吐司或白饭都合适。": "最后淋两滴香油，装盘趁热吃，配吐司或白饭都很合适。"}

for r in D:
    for s in r["steps"]:
        if s["tip"] in TIPS: s["tip"] = TIPS[s["tip"]]
        if s["cue"] in CUES: s["cue"] = CUES[s["cue"]]
        if s["t"] in TEXTS: s["t"] = TEXTS[s["t"]]
json.dump(D, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
