import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")
p = root / "data/ingredients.json"
d = json.loads(p.read_text(encoding="utf-8-sig"))
tax = json.loads((root / "data/taxonomy.json").read_text(encoding="utf-8-sig"))
valid = {x["slug"] for x in tax["allergens"]}

fixed = []
for it in d["items"]:
    bad = [a for a in it.get("allergens", []) if a not in valid]
    if bad:
        fixed.append((it["key"], bad))
        it["allergens"] = [("mollusk" if a == "shellfish" else a) for a in it["allergens"] if a in valid or a == "shellfish"]

p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("fixed:", fixed)
print("total:", len(d["items"]))
