import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\data\ingredients.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
print("TOP KEYS:", list(d.keys()))
items = d["items"]
print("first:", json.dumps(items[0], ensure_ascii=False))
for k in ["pickled-chili", "black-vinegar", "rice-vinegar", "salt", "egg"]:
    for it in items:
        if it["key"] == k:
            print(k, "->", json.dumps(it, ensure_ascii=False))
