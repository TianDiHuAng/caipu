#!/usr/bin/env node
// 生成 tasks/progress.json：按「菜系 × 品类」格子统计目标数与已完成数
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, loadTaxonomy, walkRecipeFiles, readJson } from './lib/loaders.mjs';

const taxonomy = loadTaxonomy();

// 分层目标：A 级热门（每格 15 道核心 / 8 道扩展），B 级（6/4），C 级（5/0）
const TIER = {
  A: { core: 15, ext: 8, extCount: 4 },
  B: { core: 6, ext: 4, extCount: 2 },
  C: { core: 5, ext: 0, extCount: 0 }
};

// 扩展品类优先级（按普遍适用度排序）
const EXT_PRIORITY = [
  'main-vegetable', 'main-egg', 'main-tofu', 'staple-noodle', 'staple-rice',
  'staple-bread', 'staple-porridge', 'appetizer', 'soup', 'salad',
  'snack-street', 'bakery', 'dessert', 'breakfast', 'sauce-base',
  'fermented-pickle', 'banquet', 'low-cal', 'special-diet', 'drink',
  'hotpot-bbq', 'kids', 'main-meat', 'main-poultry', 'main-seafood'
];

// 扫描现有菜谱
const actual = new Map(); // `${cuisine}|${category}` -> [ids]
for (const f of walkRecipeFiles()) {
  let d;
  try {
    d = readJson(f);
  } catch {
    continue;
  }
  if (!d?.id || !d?.cuisine?.style) continue;
  for (const c of d.category || []) {
    const k = `${d.cuisine.style}|${c}`;
    if (!actual.has(k)) actual.set(k, []);
    actual.get(k).push(d.id);
  }
}

const allCats = taxonomy.categories.map((c) => c.slug);
const regions = { cn: [], intl: [] };
let totalTarget = 0;
let totalActual = 0;
let totalCells = 0;
const tierCount = { A: 0, B: 0, C: 0 };

for (const c of taxonomy.cuisines) {
  const cfg = TIER[c.tier];
  tierCount[c.tier]++;
  const allowed = allCats.filter((x) => !c.core.includes(x) && !c.unsupported.includes(x));
  const ext = EXT_PRIORITY.filter((x) => allowed.includes(x)).slice(0, cfg.extCount);

  const cells = [];
  for (const cat of c.core) {
    const k = `${c.slug}|${cat}`;
    const ids = actual.get(k) || [];
    cells.push({ category: cat, kind: 'core', target: cfg.core, actual: ids.length, ids });
  }
  for (const cat of ext) {
    const k = `${c.slug}|${cat}`;
    const ids = actual.get(k) || [];
    cells.push({ category: cat, kind: 'ext', target: cfg.ext, actual: ids.length, ids });
  }

  // 未被核心/扩展格覆盖的品类（如自选品类）也要统计，避免已发布菜谱「不算数」
  const covered = new Set(cells.map((x) => x.category));
  const leftovers = [];
  for (const [k, ids] of actual.entries()) {
    const [cui, cat] = k.split('|');
    if (cui !== c.slug || covered.has(cat)) continue;
    leftovers.push({ category: cat, kind: 'extra', target: 0, actual: ids.length, ids });
  }
  leftovers.sort((a, b) => b.actual - a.actual);
  cells.push(...leftovers);

  const target = cells.reduce((a, x) => a + x.target, 0);
  const done = cells.reduce((a, x) => a + x.actual, 0);
  totalTarget += target;
  totalActual += done;
  totalCells += cells.length;

  regions[c.region].push({
    slug: c.slug, zh: c.zh, en: c.en, tier: c.tier,
    target, actual: done, cells
  });
}

const progress = {
  generatedAt: new Date().toISOString(),
  rule: {
    note: '目标数由 tier 推导：A 级核心品类 15 道/格、扩展 8 道/格（4 个）；B 级 6/4（2 个）；C 级 5 道/格（仅核心品类）',
    tierDistribution: tierCount
  },
  totals: {
    cuisines: taxonomy.cuisines.length,
    cells: totalCells,
    target: totalTarget,
    actual: totalActual,
    coverage: totalActual / totalTarget
  },
  regions
};

const outFile = path.join(ROOT, 'tasks', 'progress.json');
fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, JSON.stringify(progress, null, 2), 'utf8');

console.log(`progress.json 已生成：${progress.totals.cuisines} 菜系 / ${totalCells} 格 / 目标 ${totalTarget} / 已完成 ${totalActual}（${(progress.totals.coverage * 100).toFixed(1)}%）`);
