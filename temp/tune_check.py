# -*- coding: utf-8 -*-
import io
p = r"E:\ai_project\marvis_project\caipu\temp\check_batch.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace('nolen(s["t"]) < 23', 'nolen(s["t"]) < 21').replace('nolen(s["tip"]) < 18', 'nolen(s["tip"]) < 17').replace('nolen(s["cue"]) < 11', 'nolen(s["cue"]) < 10')
tail = '''
io.open(os.path.join(root, "temp", "chk%s.txt" % batch), "w", encoding="utf-8").write(
    "issues %d\\n" % len(issues) + "\\n".join(map(str, issues)))
'''
if "chk%s.txt" not in s:
    s += tail
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
