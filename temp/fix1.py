import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")

# 1) 补别名：大葱 → 葱白/葱丝
p = root / "data" / "ingredients.json"
d = json.loads(p.read_text(encoding="utf-8-sig"))
for it in d["items"]:
    if it["key"] == "welsh-onion":
        for a in ["葱白", "葱丝", "葱段"]:
            if a not in it["aliases"]:
                it["aliases"].append(a)
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

# 2) 宫保鸡丁第 6 步补入盐的使用
rp = root / "data" / "recipes" / "cn" / "sichuan" / "gongbao-jiding.json"
r = json.loads(rp.read_text(encoding="utf-8-sig"))
s6 = r["steps"][5]
assert s6["n"] == 6
s6["text"] = (
    "倒回鸡丁并转中大火，翻炒 30 秒让香料均匀裹上，再次搅动碗汁后沿锅边一次淋入，"
    "快速翻匀至汤汁收紧发亮，尝一下咸度不足时补入 2 克盐，最后倒入花生米翻两下立即关火。"
)
rp.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")

print("ok")
