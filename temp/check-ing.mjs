import fs from 'node:fs';
const d = JSON.parse(fs.readFileSync('data/ingredients.json', 'utf8'));
const arr = Array.isArray(d) ? d : d.ingredients;
const names = new Set();
for (const x of arr) {
  if (x.zh) names.add(x.zh);
  for (const a of x.aliases || []) names.add(a);
}
const cand = process.argv.slice(2);
for (const c of cand) console.log((names.has(c) ? 'OK   ' : 'MISS ') + c);
console.log('dict size', arr.length);
