import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\tasks\engineering.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
print("type:", type(d).__name__, "keys:", list(d)[:6] if isinstance(d, dict) else len(d))
print(json.dumps(d, ensure_ascii=False)[:600])
