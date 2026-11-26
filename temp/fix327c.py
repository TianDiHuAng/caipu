# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-327.json"
d=json.load(io.open(p,encoding="utf-8"))
rep={
 "chaoshan-haozi-zhou":[("青菜末最后撒","芹菜末最后撒")],
 "chaoshan-lushui-doufu":[("趁热配白米饭吃最香","趁热配热饭吃最香"),("砂锅端上桌配白饭，卤汁浇饭最香","砂锅端上桌配热乎的饭，卤汁浇饭最香")],
 "chaoshan-shacha-chao-hetiao":[("小白菜叶薄，下锅二十秒即可。","芦笋切斜段，下锅炒三十秒即可。")],
 "chaoshan-puning-doujiang-yu":[("连汁带鱼滑入盘中","连汁一起滑入盘中")],
 "chaoshan-nanjiang-ji":[("水面只能冒虾眼泡","水面只能冒细密小泡"),("鸡腿关节处渗出清亮汁水","腿根关节处渗出清亮汁水"),("用筷子扎鸡腿最厚处","用筷子扎腿根最厚处"),("鸡腿最厚处中心温度","腿根最厚处中心温度"),("用鸡腿肉浸煮时间缩到十五分钟","用去骨鸡腿块浸煮时间缩到十五分钟")],
}
def walk(o, pairs):
    if isinstance(o,str):
        for a,b in pairs: o=o.replace(a,b)
        return o
    if isinstance(o,list): return [walk(x,pairs) for x in o]
    if isinstance(o,dict): return {k:walk(v,pairs) for k,v in o.items()}
    return o
for i,r in enumerate(d):
    if r["id"] in rep:
        d[i]=walk(r,rep[r["id"]])
    if r["id"]=="chaoshan-suanrong-lajiao-jiang":
        d[i]["flavor"]=["spicy","salty","fragrant"]
        d[i]["diet_tags"]=[t for t in d[i]["diet_tags"] if t!="gluten-free"]
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixed", sum(1 for r in d if r["id"] in rep))
