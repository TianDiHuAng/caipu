import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\data\taxonomy.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
print("keys:", list(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list) and v:
        print(k, "len", len(v), "sample", json.dumps(v[0], ensure_ascii=False)[:200])
