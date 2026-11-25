# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-325.json"
d=json.load(io.open(p,encoding="utf-8")); m={r["id"]:r for r in d}
m["lanzhou-niurou-mian"]["tips"][2]="香料包别放太多，压过牛肉本味就成了卤汤，清汤的鲜就没影了。"
m["xibei-ziran-yangpai"]["steps"][5]["tip"]="静置三分钟能锁住肉汁，切的时候不流失，肉才嫩而不柴。"
m["xibei-dapanji"]["tips"][0]="鸡选两斤半的土鸡，肉质紧实耐炖，炖久了也不散架发柴。"
m["xibei-dapanji"]["tips"][1]="土豆选黄心的，炖出来绵软带甜，白心的偏水不糯。"
m["xibei-yangrou-fentang"]["steps"][1]["tip"]="浮沫撇净，汤清味才正，这一步偷懒整锅汤都带着一股腥膻气。"
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
