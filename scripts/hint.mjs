#!/usr/bin/env node
/**
 * 写作辅助：查询食材在词典中的 key / 过敏原 / 归属，并给出用量折算。
 * 用法：
 *   node scripts/hint.mjs 鸡腿肉 花生米 干辣椒 酱油
 *   node scripts/hint.mjs --amount 300g 2piece 1tbsp   # 单独折算
 */
import { loadIngredients, buildNameIndex } from './lib/loaders.mjs';
import { toGrams } from './lib/rules.mjs';

const args = process.argv.slice(2);
const dict = loadIngredients();
const idx = buildNameIndex(dict);

const amountArgs = args.filter((a) => /^[\d.]+[a-z]+$/i.test(a));
const nameArgs = args.filter((a) => !amountArgs.includes(a));

if (amountArgs.length) {
  const unitMap = { g: 'g', ml: 'ml', piece: 'piece', clove: 'clove', slice: 'slice', stalk: 'stalk', tsp: 'to-taste', tbsp: 'to-taste', cup: 'ml' };
  for (const a of amountArgs) {
    const m = a.match(/^([\d.]+)([a-z]+)$/i);
    if (!m) continue;
    const amount = Number(m[1]);
    let unit = m[2].toLowerCase();
    if (unit === 'cup') {
      console.log(`${a} ≈ ${(amount * 240).toFixed(0)} g/ml`);
      continue;
    }
    unit = unitMap[unit] ?? unit;
    console.log(`${a} → unit=${unit} grams≈${toGrams(amount, unit, null)}`);
  }
}

let allergens = new Set();
for (const name of nameArgs) {
  const hit = idx.get(name);
  if (!hit) {
    const near = dict.items.filter((i) => i.zh.includes(name) || name.includes(i.zh) || i.aliases.some((a) => a.includes(name) || name.includes(a))).slice(0, 4);
    console.log(`? ${name} → 未收录${near.length ? '，候选：' + near.map((n) => `${n.zh}(${n.key})`).join(' / ') : ''}`);
    continue;
  }
  hit.allergens.forEach((a) => allergens.add(a));
  console.log(`✓ ${name} → key=${hit.key} | category=${hit.category} | allergens=[${hit.allergens.join(',')}] | aliases=[${hit.aliases.join(',')}]`);
}
if (allergens.size) console.log(`\n合并过敏原: [${[...allergens].sort().join(', ')}]`);
