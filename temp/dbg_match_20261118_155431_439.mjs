import fs from 'fs';
const ROOT = 'D:/AI/project/marvis_project/caipu';
const dict = JSON.parse(fs.readFileSync(ROOT + '/data/ingredients.json', 'utf8').replace(/^\uFEFF/, ''));
const names = [];
for (const item of dict.items) {
  names.push([item.zh, item]);
  for (const a of item.aliases || []) if (a.length >= 2) names.push([a, item]);
}
names.sort((a, b) => b[0].length - a[0].length);
const r = JSON.parse(fs.readFileSync(ROOT + '/data/recipes/cn/sichuan/fuqi-feipian.json', 'utf8').replace(/^\uFEFF/, ''));
const text = r.steps.map(s => `${s.text} ${s.tip} ${s.visual_cue}`).join('\n');
const consumed = new Uint8Array(text.length);
const hits = [];
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
    hits.push([item.zh, name, idx, text.slice(Math.max(0, idx - 15), idx + 15)]);
  }
}
console.log(hits.map(h => h.join(' | ')).join('\n'));
