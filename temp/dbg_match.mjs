import fs from 'node:fs';
import path from 'node:path';
const root = 'D:/AI/project/marvis_project/caipu';
const dict = JSON.parse(fs.readFileSync(path.join(root, 'data/ingredients.json'), 'utf8').replace(/^\uFEFF/, ''));
const names = [];
for (const it of dict.items) {
  names.push([it.zh, it]);
  for (const a of it.aliases || []) if (a.length >= 2) names.push([a, it]);
}
names.sort((a, b) => b[0].length - a[0].length);
const file = process.argv[2];
const r = JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const text = r.steps.map((s) => `${s.text || ''} ${s.tip || ''} ${s.visual_cue || ''}`).join('\n');
const consumed = new Uint8Array(text.length);
for (const [name, item] of names) {
  let from = 0;
  for (;;) {
    const idx = text.indexOf(name, from);
    if (idx === -1) break;
    from = idx + name.length;
    let free = true;
    for (let i = idx; i < idx + name.length; i++) if (consumed[i]) { free = false; break; }
    if (!free) continue;
    for (let i = idx; i < idx + name.length; i++) consumed[i] = 1;
    if (item.zh.includes('肉') || name.includes('肉')) {
      console.log(`HIT name=${name} item=${item.zh} ctx=...${text.slice(Math.max(0, idx - 20), idx + 20).replace(/\n/g, ' / ')}...`);
    }
  }
}
