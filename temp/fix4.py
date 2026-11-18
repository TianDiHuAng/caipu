from pathlib import Path
import re

root = Path(r"D:\AI\project\marvis_project\caipu") / "apps" / "api" / "src"
pat = re.compile(r"(?<!\.)\bdb\.(select|insert|update|delete|execute|run|all|get|prepare)\(")
for f in sorted(root.rglob("*.ts")):
    s = f.read_text(encoding="utf-8")
    n = len(pat.findall(s))
    if n:
        print(f"{f.relative_to(root)}: {n}")
        s2 = pat.sub(lambda m: f"db.db.{m.group(1)}(", s)
        f.write_text(s2, encoding="utf-8")
print("done")
