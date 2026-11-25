
import fs from 'fs';
const dict=JSON.parse(fs.readFileSync('data/ingredients.json','utf8'));
const r=JSON.parse(fs.readFileSync('data/recipes/cn/sichuan/sichuan-tudou-menfan.json','utf8'));
const t=(r.steps||[]).map(s=>`${s.text||''} ${s.tip||''} ${s.visual_cue||''}`).join('\n');
const names=[];
for(const it of dict.items){ names.push([it.zh,it]); for(const a of it.aliases||[]) if(a.length>=2) names.push([a,it]); }
names.sort((a,b)=>b[0].length-a[0].length);
const consumed=new Uint8Array(t.length); const hit=new Map();
for(const [name,item] of names){
  let from=0;
  for(;;){
    const idx=t.indexOf(name,from); if(idx===-1) break; from=idx+name.length;
    let free=true; for(let i=idx;i<idx+name.length;i++){ if(consumed[i]){free=false;break;} }
    if(!free) continue;
    for(let i=idx;i<idx+name.length;i++) consumed[i]=1;
    hit.set(item.zh,(hit.get(item.zh)||[]).concat([[name,idx]]));
  }
}
console.log([...hit.keys()].join(','));
if(hit.get('油豆腐')) { for(const [n,i] of hit.get('油豆腐')) console.log('HIT',n,i,JSON.stringify(t.slice(Math.max(0,i-30),i+20))); }
