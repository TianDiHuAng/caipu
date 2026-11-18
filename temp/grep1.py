from pathlib import Path
import re

root = Path(r"D:\AI\project\marvis_project\caipu")
for f in root.rglob("*.mjs"):
    if "node_modules" in str(f):
        continue
    s = f.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(s.splitlines(), 1):
        if "配料表中没有" in line or "mentioned" in line or "stepScopeText" in line or "allText" in line:
            print(f"{f.relative_to(root)}:{i}: {line.strip()[:140]}")
