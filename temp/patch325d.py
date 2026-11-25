# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-325.json"
d=json.load(io.open(p,encoding="utf-8")); m={r["id"]:r for r in d}

r=m["lanzhou-niurou-mian"]
r["steps"][0]["t"]="牛骨敲断冷水浸泡一小时去血水，牛肉也泡半小时，中途换两次水。"
r["steps"][0]["cue"]="骨头断面发白，泡出的水色淡红"
r["steps"][1]["t"]="牛骨与牛肉冷水下锅焯水，煮开撇净浮沫，捞出用温水冲净表面。"
r["steps"][2]["t"]="汤锅加足量清水，放牛骨、牛肉、姜片、葱段、花椒、八角、桂皮与香叶，大火烧开。"
r["steps"][3]["t"]="转小火慢炖两小时，炖到筷子能轻松插透牛肉，捞出牛肉晾凉切片。"
r["steps"][3]["cue"]="汤色转清亮，筷子一插即透"
r["steps"][6]["t"]="碗中码上牛肉片与萝卜片，浇滚汤没过碗里的面，撒蒜苗末与香菜，淋辣椒油。"

c=m["xibei-cuoyuzi"]
c["steps"][2]["t"]="取一根粗面棍在案板上用手掌搓成两头尖、中间粗的小鱼形状，依次搓完。"
c["steps"][7]["t"]="面鱼趁热倒入炒锅，加青椒丝翻匀，淋米醋与辣椒油，撒香菜出锅。"

f=m["xibei-yangrou-fentang"]
f["ingredients"][2]["items"]=[x for x in f["ingredients"][2]["items"] if x["n"]!="植物油"]

json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
