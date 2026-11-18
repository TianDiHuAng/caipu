import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")
tax = json.loads((root / "data/taxonomy.json").read_text(encoding="utf-8-sig"))
for k in ["flavors", "dietTags", "allergens"]:
    print(k, ":", ",".join(x["slug"] for x in tax[k]))
print("categories:", ",".join(x["slug"] for x in tax["categories"]))
