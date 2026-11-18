import json
from pathlib import Path
ROOT = Path(r"D:\AI\project\marvis_project\caipu")
items = json.loads((ROOT / "data/ingredients.json").read_text(encoding="utf-8-sig"))["items"]
by = {}
for it in items:
    by.setdefault(it["category"], []).append(it["zh"])
for k, v in by.items():
    print(k, len(v), "：", " ".join(v))
