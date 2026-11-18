from pathlib import Path
import re

root = Path(r"D:\AI\project\marvis_project\caipu") / "apps" / "api" / "src"
pat = re.compile(r"(?<![\w.])db(\s*)\.(select|insert|update|delete|execute|run)\b")
for f in sorted(root.rglob("*.ts")):
    s = f.read_text(encoding="utf-8")
    s2, n = pat.subn(lambda m: f"db.db{m.group(1)}.{m.group(2)}", s)
    if n:
        f.write_text(s2, encoding="utf-8")
        print(f"{f.relative_to(root)}: {n}")
print("done")
