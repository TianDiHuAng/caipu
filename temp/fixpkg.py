import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\package.json")
raw = p.read_text(encoding="utf-8-sig")
d = json.loads(raw)
d["scripts"]["test"] = "node --import tsx --test --test-reporter=spec tests/"
d["scripts"]["test:quick"] = "node --test tests/data.test.mjs"
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(d["scripts"]["test"])
print("BOM:", p.read_bytes()[:3] == b"\xef\xbb\xbf")
