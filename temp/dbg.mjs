import fs from 'node:fs';

const p = 'D:/AI/project/marvis_project/caipu/data/recipes/cn/sichuan/mapo-doufu.json';
const r = JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const stepScope = r.steps.map((s) => `${s.text} ${s.tip} ${s.visual_cue}`).join('\n');
for (const kw of ['北豆腐', '猪肉末', '嫩豆腐', '豆腐块', '豆腐']) {
  const idx = stepScope.indexOf(kw);
  console.log(kw, idx, idx >= 0 ? JSON.stringify(stepScope.slice(Math.max(0, idx - 15), idx + 15)) : '');
}
console.log('---steps text sample---');
console.log(stepScope.slice(0, 300));
