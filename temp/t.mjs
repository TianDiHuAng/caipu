import fs from "fs";
const dict=JSON.parse(fs.readFileSync("data/ingredients.json","utf8"));
const r=JSON.parse(fs.readFileSync("data/recipes/cn/sichuan/tudou-shao-paigu.json","utf8"));
const text=r.steps.map(s=>`${s.text||""} ${s.tip||""} ${s.visual_cue||""}`).join("\n");
const names=[];
for(const it of dict.items){names.push([it.zh,it]); for(const a of it.aliases||[]) if(a.length>=2) names.push([a,it]);}
names.sort((a,b)=>b[0].length-a[0].length);
const consumed=new Uint8Array(text.length); const hit=new Set();
for(const [name,item] of names){let from=0;for(;;){const idx=text.indexOf(name,from); if(idx===-1)break; from=idx+name.length; let free=true; for(let i=idx;i<idx+name.length;i++){if(consumed[i]){free=false;break;}} if(!free)continue; for(let i=idx;i<idx+name.length;i++)consumed[i]=1; hit.add(item);}}
for(const h of hit) console.log(h.key, h.zh);
