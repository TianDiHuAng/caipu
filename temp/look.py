import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")
tax = json.loads((root / "data/taxonomy.json").read_text(encoding="utf-8-sig"))
print("CUISINES:")
for c in tax["cuisines"]:
    print(f'  {c["slug"]}({c["zh"]},tier{c["tier"]}) core={",".join(c.get("core", []))}')

ing = json.loads((root / "data/ingredients.json").read_text(encoding="utf-8-sig"))
items = ing["items"] if isinstance(ing, dict) else ing
print("\nINGREDIENT COUNT:", len(items))

names = ["三黄鸡", "鸡", "鲤鱼", "鳝鱼", "五花肉", "青椒", "剁椒", "笋", "鸡蛋", "西红柿", "番茄",
         "海参", "大白菜", "醋", "冰糖", "生抽", "老抽", "蚝油", "郫县豆瓣", "豆豉", "蒜苗",
         "土豆", "茄子", "豆角", "五花肉", "排骨", "牛腩", "羊肉", "虾仁", "豆腐", "香菇", "木耳"]
idx = {}
for it in items:
    for k in [it["zh"]] + it.get("aliases", []):
        idx.setdefault(k, it["key"])
print("\nLOOKUP:")
for n in names:
    print(f"  {n} -> {idx.get(n)}")
