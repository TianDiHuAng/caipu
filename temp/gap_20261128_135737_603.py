# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = json.load(open(r'E:\ai_project\marvis_project\caipu\tasks\progress.json', encoding='utf-8'))
print(list(p.keys()))
r = p['regions'][0]
print(list(r.keys()))
print(json.dumps(r, ensure_ascii=False)[:400])
rows = []
for reg in p['regions']:
    for key in ('cuisines', 'items'):
        for c in reg.get(key, []) or []:
            if not isinstance(c, dict):
                continue
            t = c.get('actual', c.get('done', 0))
            g = c.get('target', 0)
            if g and t < g:
                rows.append((g - t, c.get('slug') or c.get('name'), t, g))
rows.sort(reverse=True)
print(rows[:14])
