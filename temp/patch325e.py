# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-325.json"
d=json.load(io.open(p,encoding="utf-8")); m={r["id"]:r for r in d}
m["lanzhou-niurou-mian"]["steps"][5]["cue"]="碱性面身弹性足，挑起不断条"
m["xibei-cuoyuzi"]["steps"][1]["cue"]="面棍粗细一致，断面方正平整"
m["xibei-cuoyuzi"]["steps"][7]["cue"]="汤汁裹满面鱼，青椒翠绿不黄"
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
