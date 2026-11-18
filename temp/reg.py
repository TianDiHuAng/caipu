import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")
tax = json.loads((root / "data/taxonomy.json").read_text(encoding="utf-8-sig"))
print("REGIONS:", json.dumps(tax["regions"], ensure_ascii=False))
ing = json.loads((root / "data/ingredients.json").read_text(encoding="utf-8-sig"))["items"]
idx = {}
for it in ing:
    for k in [it["zh"]] + it.get("aliases", []):
        idx[k] = it["key"]
for n in ["鸡腿肉", "三黄鸡", "冰糖", "笋", "蒜苗", "豆豉", "郫县豆瓣", "酱油", "料酒", "菜籽油",
          "香油", "芝麻油", "姜", "大葱", "蒜", "白糖", "玉米淀粉", "盐", "花椒", "香醋"]:
    print(n, "->", idx.get(n))
