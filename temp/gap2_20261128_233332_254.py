import json
p = json.load(open('tasks/progress.json', encoding='utf-8'))
rows = []
for rid, lst in p['regions'].items():
    for c in lst:
        cells = c.get('cells') or []
        gap = sum(max(0, x.get('target', 0) - x.get('actual', 0)) for x in cells)
        if gap > 0:
            detail = ['%s:%d' % (x['category'], x['target'] - x['actual'])
                      for x in cells if x.get('target', 0) > x.get('actual', 0)]
            rows.append((gap, rid, c['slug'], sum(x.get('target', 0) for x in cells), sum(x.get('actual', 0) for x in cells), detail))
rows.sort(key=lambda x: -x[0])
out = ['total gap %d, cuisines %d' % (sum(r[0] for r in rows), len(rows))]
for gap, rid, slug, t, a, detail in rows[:15]:
    out.append('%s(%s) gap=%d  %d/%d  %s' % (slug, rid, gap, a, t, ', '.join(detail)))
open('temp/gap.txt', 'w', encoding='utf-8').write('\n'.join(out))
