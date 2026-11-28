const fs = require('fs');
const p = JSON.parse(fs.readFileSync('tasks/progress.json', 'utf8'));
const out = [];
out.push('region keys: ' + Object.keys(p.regions[0]).join(','));
const rows = [];
for (const reg of p.regions) {
  const cs = reg.cuisines || reg.items || reg.grid || [];
  for (const c of cs) {
    if ((c.actual || 0) < (c.target || 0)) rows.push([c.slug, c.actual, c.target]);
  }
}
rows.sort((a, b) => (a[1] - a[2]) - (b[1] - b[2]));
out.push('gap total ' + rows.reduce((s, x) => s + (x[2] - x[1]), 0) + ' cuisines ' + rows.length);
for (const r of rows.slice(0, 12)) out.push(r.join(' / '));
fs.writeFileSync('temp/gap.txt', out.join('\n'), 'utf8');
console.log('done');
