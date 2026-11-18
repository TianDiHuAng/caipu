import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\data\ingredients.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
for it in d["items"]:
    if it["key"] in ("black-vinegar", "rice-vinegar"):
        print(it["key"], it["zh"], it["aliases"])
        if it["key"] == "black-vinegar":
            it["aliases"] = [a for a in it["aliases"] if a != "米醋"]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("fixed")
