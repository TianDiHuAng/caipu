import fs from 'node:fs';
const p = JSON.parse(fs.readFileSync('tasks/progress.json', 'utf8'));
const rows = [];
for (const [region, v] of Object.entries(p.regions)) {
  if (!v || !v.cells) continue;
  for (const c of v.cells) {
    if (c.target > 0 && c.actual < c.target) {
      rows.push([region, v.slug, v.zh, c.category, c.target - c.actual, c.actual, c.target]);
    }
  }
}
rows.sort((a, b) => b[4] - a[4]);
console.log(rows.slice(0, 50).map(r => r.join(' | ')).join('\n'));
console.log('total gap cells:', rows.length);
