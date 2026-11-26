# -*- coding: utf-8 -*-
import json,io,os,glob
os.chdir(r"E:\ai_project\marvis_project\caipu")
print("== chaoshan 现有")
for p in glob.glob("data/recipes/cn/chaoshan/*.json"):
    j=json.load(io.open(p,encoding="utf-8"))
    print(os.path.basename(p)[:-5], j["title_zh"] if "title_zh" in j else j.get("name_zh",""), j["category"])
print("== taxonomies chaoshan")
t=json.load(io.open("data/taxonomy.json",encoding="utf-8"))
for c in t["cuisines"]:
    if c["slug"]=="chaoshan": print(json.dumps(c,ensure_ascii=False))
print("== 品类")
for c in t["categories"]: print(c["slug"], c.get("name_zh") or c.get("zh"))
print("== 食材核对")
ing=json.load(io.open("data/ingredients.json",encoding="utf-8"))
names={}
for it in ing["items"]:
    for k in [it["zh"]]+(it.get("aliases") or []): names[k]=it["zh"]
for w in ["沙茶酱","鱼露","南姜","普宁豆酱","粿条","芥蓝","血蚶","薄壳","生蚝","蚝","潮州酸菜","咸菜","橄榄菜","九层塔","紫菜","鱼丸","牛肉丸","猪血","腐竹","菜脯","冬菜","虾米","冬瓜","苦瓜","芋头","糯米","花生","芝麻","梅菜","南乳","陈皮","甘草","香茅","沙姜","三奈","葱","小葱","大蒜","姜","香菜","红葱头","猪肠","猪皮","鱼片","马鲛鱼","鲳鱼","黄鱼","鱿鱼","蛤蜊","花蛤","鸭","整鸡","鹅肉","五花肉","牛肉","牛腩","猪肉末","猪蹄"]:
    print(w, "登记" if w in names else "未登记", names.get(w,""))
