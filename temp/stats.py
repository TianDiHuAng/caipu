# -*- coding: utf-8 -*-
import json, glob, collections, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
tx=json.load(io.open("data/taxonomy.json",encoding="utf-8"))
cu={c["slug"]:c for c in tx["cuisines"]}
cnt=collections.Counter()
for f in glob.glob(os.path.join("data","recipes","*","*","*.json")):
    parts=f.replace("\\","/").split("/")
    cnt[parts[-2]]+=1
print("used",len(cnt),"total",sum(cnt.values()))
for s,c in cnt.most_common()[-20:]:
    print(s,c,cu[s]["zh"],"|"," ".join(cu[s]["core"]))
