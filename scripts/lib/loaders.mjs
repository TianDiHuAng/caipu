import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export function readJson(p) {
  const raw = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
  return JSON.parse(raw);
}

export function loadTaxonomy() {
  return readJson(path.join(ROOT, 'data', 'taxonomy.json'));
}

export function loadIngredients() {
  return readJson(path.join(ROOT, 'data', 'ingredients.json'));
}

export function loadSchema() {
  return readJson(path.join(ROOT, 'schema', 'recipe.schema.json'));
}

export const RECIPES_DIR = path.join(ROOT, 'data', 'recipes');

/** 递归列出所有菜谱 JSON 文件 */
export function walkRecipeFiles(dir = RECIPES_DIR, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('_') || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkRecipeFiles(full, acc);
    else if (entry.isFile() && entry.name.endsWith('.json')) acc.push(full);
  }
  return acc.sort();
}

export function relPath(p) {
  return path.relative(ROOT, p).replace(/\\/g, '/');
}

/** 构建食材名索引：zh 名与所有别名 -> 词典条目 */
export function buildNameIndex(dict) {
  const index = new Map();
  for (const item of dict.items) {
    index.set(item.zh, item);
    for (const a of item.aliases || []) index.set(a, item);
    if (!index.has(item.en)) index.set(item.en, item);
  }
  return index;
}

export function buildKeyIndex(dict) {
  const index = new Map();
  for (const item of dict.items) index.set(item.key, item);
  return index;
}

/** 校验分类体系与食材词典的内部一致性 */
export function checkTaxonomyConsistency(taxonomy, dict) {
  const errors = [];
  const cats = new Set(taxonomy.categories.map((c) => c.slug));
  const cuisines = new Set();
  for (const c of taxonomy.cuisines) {
    if (cuisines.has(c.slug)) errors.push(`taxonomy: 菜系 slug 重复 ${c.slug}`);
    cuisines.add(c.slug);
    for (const s of c.core) if (!cats.has(s)) errors.push(`taxonomy: ${c.slug} 的核心品类 ${s} 不存在`);
    for (const s of c.unsupported) {
      if (!cats.has(s)) errors.push(`taxonomy: ${c.slug} 的排除品类 ${s} 不存在`);
      if (c.core.includes(s)) errors.push(`taxonomy: ${c.slug} 的品类 ${s} 同时被列为核心与排除`);
    }
    if (c.core.length < 3) errors.push(`taxonomy: ${c.slug} 核心品类少于 3 个`);
    if (c.tier !== 'A' && c.tier !== 'B' && c.tier !== 'C') errors.push(`taxonomy: ${c.slug} tier 非法`);
  }
  const keys = new Set();
  const names = new Set();
  for (const item of dict.items) {
    if (keys.has(item.key)) errors.push(`ingredients: key 重复 ${item.key}`);
    keys.add(item.key);
    if (names.has(item.zh)) errors.push(`ingredients: 中文名重复 ${item.zh}`);
    names.add(item.zh);
    if (!Array.isArray(item.allergens)) errors.push(`ingredients: ${item.key} 缺少 allergens 数组`);
  }
  return errors;
}
