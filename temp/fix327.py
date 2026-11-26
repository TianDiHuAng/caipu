# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-327.json"
d=json.load(io.open(p,encoding="utf-8"))
D={r["id"]:r for r in d}

r=D["chaoshan-haozi-zhou"]; r["prep"]=45; r["cook"]=50
r["steps"][6]["t"]="关火撒芹菜末、小葱切成的葱花与香菜段，淋香油搅匀，连锅端上桌趁热吃。"

r=D["chaoshan-shacha-chao-hetiao"]
for s in r["steps"]:
    if s["cue"]=="芥蓝翠绿，豆芽略塌": s["cue"]="芥蓝翠绿挺立，豆芽略塌微软"
    if "蒜末" in s["t"]: s["t"]=s["t"].replace("下蒜末","下大蒜末")

r=D["chaoshan-nanjiang-ji"]; r["prep"]=40; r["cook"]=45
for s in r["steps"]:
    if s["cue"]=="冰水清澈，盆壁结霜": s["cue"]="冰水清澈见底，盆壁凝出一层薄霜"
    if s["t"].startswith("南姜磨成细末"): s["t"]="南姜磨成细末，加盐八克、鱼露、白胡椒与香油调成蘸料，另备一小碟原汤。"

r=D["chaoshan-lushui-doufu"]; r["cook"]=35
for s in r["steps"]:
    if s["cue"]=="汤色红亮，香气浓郁": s["cue"]="汤色红亮油润，香料香气浓郁"
    if "葱结" in s["t"]: s["t"]=s["t"].replace("葱结","小葱结")
    if s["t"]=="关火撒香菜段，连砂锅端上桌，趁热配白饭。": s["t"]="关火撒上香菜段，连砂锅端上桌，趁热配白米饭吃最香。"

r=D["chaoshan-jiucai-zhuxie-tang"]
for s in r["steps"]:
    t=s["t"]
    if t=="汤锅加清水九百毫升，放姜丝大火烧开。":
        s["t"]="汤锅放植物油，下姜丝小火煸出香味，加清水九百毫升转大火烧开。"
        s["cue"]="水面翻滚，姜香与油香飘出"
    if t=="下猪血块，转中火煮八分钟，其间撇净浮沫。":
        s["t"]="下猪血块，转中火煮八分钟，其间用汤勺撇净表面浮沫。"
    if t=="加盐与鱼露调味，搅匀后尝一口汤的咸淡。":
        s["t"]="加盐与鱼露调味，搅匀后先尝一口汤的咸淡，再决定是否补盐。"
    if t=="淋香油，撒白胡椒与葱花，盛入大碗趁热喝。":
        s["t"]="淋香油，撒白胡椒与小葱切成的葱花，盛入大碗趁热喝。"
        s["cue"]="热气腾腾，胡椒与葱香扑鼻"
    if t=="韭菜段下锅，保持中火煮一分半，见叶片转深绿立刻关火。":
        s["cue"]="韭菜碧绿挺立，汤面浮起油花"

r=D["chaoshan-puning-doujiang-yu"]; r["cook"]=30
for s in r["steps"]:
    if s["cue"]=="鱼身干爽，刀口齐整": s["cue"]="鱼身干爽无水光，刀口齐整"
    if s["cue"]=="两面金黄，鱼身完整": s["cue"]="两面金黄焦香，鱼身完整不破"
    if "蒜末" in s["t"]: s["t"]=s["t"].replace("下姜片、蒜末","下姜片、大蒜末")
    if "撒葱段" in s["t"]: s["t"]=s["t"].replace("撒葱段","撒小葱段")

r=D["chaoshan-suanrong-lajiao-jiang"]; r["prep"]=140; r["cook"]=30

json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixed")
