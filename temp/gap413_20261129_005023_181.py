# -*- coding: utf-8 -*-
import json

p = json.load(open('tasks/progress.json', encoding='utf-8'))
r0 = p['regions'][0]
rows = []
def walk(o, path=''):
    if isinstance(o, dict):
        if 'target' in o and 'done' in o:
            g = o.get('target', 0) - o.get('done', 0)
            if g > 0:
                rows.append((g, o.get('slug') or o.get('name') or path, o.get('done'), o.get('target')))
            return
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path)
walk(p)
rows.sort(reverse=True)
print('总缺口', sum(x[0] for x in rows), '条目', len(rows))
seen = set()
for g, s, d, t in rows:
    if s in seen:
        continue
    seen.add(s)
    print(g, s, d, t)
    if len(seen) >= 16:
        break
