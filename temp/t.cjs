
import fs from 'fs';
const r=JSON.parse(fs.readFileSync('data/recipes/cn/sichuan/sichuan-tudou-menfan.json','utf8'));
const parts=[];
for(const s of r.steps||[]) parts.push(s.text||'', s.tip||'', s.visual_cue||'');
parts.push(...(r.tips||[])); parts.push(...(r.common_mistakes||[])); parts.push(...(r.substitutions||[])); parts.push(...(r.variations||[]));
parts.push(r.serving_suggestion||'', r.storage||'', r.food_safety_notes||'', r.origin_note||'');
const t=parts.join('\n');
const i=t.indexOf('油豆腐');
console.log('idx',i);
if(i>=0) console.log(JSON.stringify(t.slice(i-40,i+20)));
console.log('has 油豆', t.includes('油豆'));
