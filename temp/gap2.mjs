import fs from 'node:fs';
const p = JSON.parse(fs.readFileSync('tasks/progress.json', 'utf8'));
const out = [];
for (const [region, list] of Object.entries(p.regions)) {
  if (!Array.isArray(list)) continue;
  for (const v of list) {
    for (const c of v.cells || []) {
      if (c.target > 0 && c.actual < c.target) {
        out.push({ region, slug: v.slug, zh: v.zh, cat: JSON.stringify(c.category), gap: c.target - c.actual, actual: c.actual, target: c.target });
      }
    }
  }
}
out.sort((a, b) => b.gap - a.gap);
fs.writeFileSync('temp/gaps.json', JSON.stringify(out, null, 1), 'utf8');
for (const r of out.slice(0, 60)) console.log(`${r.region}/${r.slug}(${r.zh}) ${r.cat} gap=${r.gap} ${r.actual}/${r.target}`);
console.log('cells', out.length);
