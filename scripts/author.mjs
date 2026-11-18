#!/usr/bin/env node
// 菜谱撰写工具：把「紧凑草稿」展开成符合 schema/recipe.schema.json 的完整菜谱文件。
// 目的不是批量生成内容，而是把结构样板（分组、单位、过敏原推导、总分时长、路径）交给脚本，
// 让作者只写真正的烹饪内容，减少结构错误与重复劳动。
//
// 用法：
//   npx tsx scripts/author.mjs temp/drafts/batch-01.json          # 写入
//   npx tsx scripts/author.mjs temp/drafts/batch-01.json --dry    # 只校验不写盘
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const draftPath = process.argv[2];
const dry = process.argv.includes('--dry');
if (!draftPath) {
  console.error('用法: node scripts/author.mjs <draft.json> [--dry]');
  process.exit(1);
}

const taxonomy = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'taxonomy.json'), 'utf8'));
const dict = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'ingredients.json'), 'utf8'));
const cuisineBySlug = new Map(taxonomy.cuisines.map((c) => [c.slug, c]));
const ingredientByName = new Map();
for (const it of dict.items) {
  ingredientByName.set(it.zh, it);
  for (const a of it.aliases || []) if (!ingredientByName.has(a)) ingredientByName.set(a, it);
}

const drafts = JSON.parse(fs.readFileSync(path.resolve(ROOT, draftPath), 'utf8').replace(/^\uFEFF/, ''));
const today = new Date().toISOString().slice(0, 10);
const problems = [];
const written = [];

const GROUP_ZHS = { main: '主料', aux: '辅料', seasoning: '调料' };

for (const d of drafts) {
  const label = d.id || d.zh || '(无 id)';
  const cuisine = cuisineBySlug.get(d.cuisine);
  if (!cuisine) {
    problems.push(`${label}: 菜系 ${d.cuisine} 不在 taxonomy`);
    continue;
  }

  const allergens = new Set();
  const ingredientGroups = [];
  let unknown = [];
  for (const group of d.ingredients || []) {
    const items = [];
    for (const it of group.items || []) {
      const entry = ingredientByName.get(it.n);
      if (!entry) {
        unknown.push(it.n);
        continue;
      }
      for (const a of entry.allergens || []) allergens.add(a);
      const row = {
        name: entry.zh,
        name_en: entry.en,
        amount: it.a,
        unit: it.u,
        note: it.note,
        optional: it.optional === true
      };
      if (it.substitute) row.substitute = it.substitute;
      items.push(row);
    }
    if (items.length) ingredientGroups.push({ group: group.group, items });
  }
  if (unknown.length) {
    problems.push(`${label}: 食材未登记 → ${[...new Set(unknown)].join('、')}`);
    continue;
  }

  const steps = (d.steps || []).map((s, i) => ({
    n: i + 1,
    text: s.t,
    time_min: s.time,
    heat: s.heat,
    tip: s.tip,
    visual_cue: s.cue
  }));

  const recipe = {
    schema_version: '1.0',
    content_version: 1,
    id: d.id,
    name: { zh: d.zh, en: d.en, ...(d.original ? { original: d.original } : {}) },
    cuisine: { region: cuisine.region, style: d.cuisine },
    category: d.category,
    difficulty: d.difficulty,
    time: { prep_min: d.prep, cook_min: d.cook, total_min: (d.prep || 0) + (d.cook || 0) },
    servings: d.servings,
    flavor: d.flavor,
    ingredients: ingredientGroups,
    equipment: d.equipment || [],
    steps,
    tips: d.tips || [],
    common_mistakes: d.mistakes || [],
    substitutions: (d.subs || []).map((s) => ({ original: s.orig, substitute: s.sub, ratio: s.ratio, note: s.note })),
    variations: d.variations || [],
    serving_suggestion: d.serving,
    storage: d.storage,
    nutrition_estimate: {
      basis: d.nutrition?.basis,
      calories_kcal: d.nutrition?.kcal,
      protein_g: d.nutrition?.protein,
      fat_g: d.nutrition?.fat,
      carbs_g: d.nutrition?.carbs,
      sodium_mg: d.nutrition?.sodium,
      is_estimate: true,
      disclaimer: d.nutrition?.disclaimer || '按配料表用量与常见食材成分表推算，实际数值随品牌与烹饪损耗浮动。'
    },
    allergens: [...allergens].sort(),
    diet_tags: d.diet || [],
    food_safety_notes: d.safety || [],
    origin_note: d.origin,
    tags: d.tags || [],
    related_ids: d.related || [],
    image_url: null,
    image_credit: null,
    status: 'published',
    created_at: today,
    updated_at: today
  };

  const rel = path.join('data', 'recipes', recipe.cuisine.region, recipe.cuisine.style, `${recipe.id}.json`);
  const abs = path.join(ROOT, rel);
  if (fs.existsSync(abs) && !d.overwrite) {
    problems.push(`${label}: ${rel} 已存在，跳过（草稿需显式 overwrite: true 才覆盖）`);
    continue;
  }
  if (!dry) {
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, JSON.stringify(recipe, null, 2) + '\n', 'utf8');
  }
  written.push(rel);
}

console.log(JSON.stringify({ drafts: drafts.length, written: written.length, files: written, problems }, null, 2));
process.exit(problems.length ? 2 : 0);
