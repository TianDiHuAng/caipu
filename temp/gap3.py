# -*- coding: utf-8 -*-
import json, io, sys, traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = json.load(open(r'E:\ai_project\marvis_project\caipu\tasks\progress.json', encoding='utf-8'))
rows = []
for regname, clist in p['regions'].items():
    for c in clist:
        t = c.get('actual', 0); g = c.get('target', 0)
        if t < g:
            gaps = [(x['category'], x['target'] - x['actual']) for x in c.get('cells', []) if x['actual'] < x['target']]
            rows.append((g - t, regname, c['slug'], t, g, gaps))
rows.sort(reverse=True)
print('总缺口格数前 12：')
for n, reg, slug, t, g, gaps in rows[:12]:
    print(f'{slug:<16}{t}/{g} 缺{n}  ' + ' '.join(f'{a}+{b}' for a, b in gaps))
print('总计', sum(r[0] for r in rows))
