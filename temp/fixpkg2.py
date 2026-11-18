import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\package.json")
d = json.loads(p.read_text(encoding="utf-8"))
d["scripts"]["test"] = "node --import tsx --test --test-reporter=spec \"tests/*.test.mjs\""
d["scripts"]["check"] = "node scripts/validate.mjs && npm test"
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(d["scripts"]["test"])
