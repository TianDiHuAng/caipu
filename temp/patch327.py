# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-327.json"
d=json.load(io.open(p,encoding="utf-8"))
for r in d:
    if r["id"]=="chaoshan-nanjiang-ji":
        for s in r["steps"]:
            s["t"]=s["t"].replace("腹腔塞入南姜碎、葱结与姜片","腹腔塞入南姜碎、小葱结与姜片")
    if r["id"]=="chaoshan-jiucai-zhuxie-tang":
        for s in r["steps"]:
            if s["cue"]=="汤色清亮，咸鲜适口": s["cue"]="汤色清亮见底，咸鲜适口"
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("patched")
