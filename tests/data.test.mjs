import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { readJson, walkRecipeFiles, buildNameIndex, buildKeyIndex } from '../scripts/lib/loaders.mjs';
import { validate } from '../scripts/lib/schema-lite.mjs';
import { runRecipeRules, runGlobalRules, runDuplicateCheck, buildContext } from '../scripts/lib/rules.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const taxonomy = readJson(path.join(ROOT, 'data', 'taxonomy.json'));
const dict = readJson(path.join(ROOT, 'data', 'ingredients.json'));
const schema = readJson(path.join(ROOT, 'schema', 'recipe.schema.json'));
const ctx = buildContext(taxonomy, dict);

const records = walkRecipeFiles(path.join(ROOT, 'data', 'recipes')).map((file) => ({
  file,
  rel: path.relative(ROOT, file).split(path.sep).join('/'),
  data: readJson(file),
}));

test('至少存在 3 道样板菜谱', () => {
  assert.ok(records.length >= 3, `实际 ${records.length} 道`);
});

test('每道菜谱都通过 JSON Schema 校验', () => {
  const problems = [];
  for (const r of records) {
    const errs = validate(schema, r.data);
    for (const e of errs) problems.push(`${r.rel}: ${e}`);
  }
  assert.deepEqual(problems, []);
});

test('每道菜谱都通过单文件质量规则', () => {
  const problems = [];
  for (const r of records) {
    const errs = runRecipeRules(r.data, ctx);
    for (const e of errs) problems.push(`${r.rel}: ${e}`);
  }
  assert.deepEqual(problems, []);
});

test('跨文件规则：id 唯一、路径一致、related_ids 有效', () => {
  const errs = runGlobalRules(records);
  assert.deepEqual(errs, []);
});

test('跨菜谱文本雷同检测通过', () => {
  const errs = runDuplicateCheck(records);
  assert.deepEqual(errs, []);
});

test('食材词典 key 与中文名唯一', () => {
  const keys = new Set();
  const zhs = new Map();
  const dup = [];
  for (const it of dict.items) {
    if (keys.has(it.key)) dup.push(`key 重复: ${it.key}`);
    keys.add(it.key);
    if (zhs.has(it.zh)) dup.push(`中文名重复: ${it.zh} (${zhs.get(it.zh)} / ${it.key})`);
    else zhs.set(it.zh, it.key);
  }
  assert.deepEqual(dup, []);
});

test('食材词典别名全局唯一（避免同一名称指向两个食材）', () => {
  const owner = new Map();
  const conflicts = [];
  for (const it of dict.items) {
    const names = [[it.zh, it.key], ...(it.aliases || []).map((a) => [a, it.key])];
    for (const [name, key] of names) {
      if (!name) continue;
      if (owner.has(name) && owner.get(name) !== key) {
        conflicts.push(`「${name}」同时属于 ${owner.get(name)} 与 ${key}`);
      } else {
        owner.set(name, key);
      }
    }
  }
  assert.deepEqual(conflicts, []);
});

test('菜谱引用的食材全部在词典中登记（含过敏原可推导）', () => {
  const idx = buildNameIndex(dict);
  const missing = [];
  for (const r of records) {
    for (const g of r.data.ingredients || []) {
      for (const it of g.items || []) {
        if (!idx.has(it.name)) missing.push(`${r.data.id}: ${it.name}`);
      }
    }
  }
  assert.deepEqual(missing, []);
});

test('分类体系与菜谱引用一致', () => {
  const catSlugs = new Set(taxonomy.categories.map((c) => c.slug));
  const cuisineSlugs = new Set(taxonomy.cuisines.map((c) => c.slug));
  const bad = [];
  for (const r of records) {
    for (const c of r.data.category || []) if (!catSlugs.has(c)) bad.push(`${r.data.id}: 未知品类 ${c}`);
    if (!cuisineSlugs.has(r.data.cuisine.style)) bad.push(`${r.data.id}: 未知菜系 ${r.data.cuisine.style}`);
  }
  assert.deepEqual(bad, []);
});

test('progress.json 结构完整且覆盖全部菜系×品类格子', () => {
  const progress = readJson(path.join(ROOT, 'tasks', 'progress.json'));
  const regions = progress.regions || {};
  const cells = [];
  for (const list of Object.values(regions)) {
    for (const c of list) {
      assert.ok(c.slug && Array.isArray(c.cells), '菜系节点需含 slug 与 cells');
      for (const cell of c.cells) {
        cells.push({ cuisine: c.slug, ...cell });
      }
    }
  }
  const uniqueCells = new Set(cells.map((c) => `${c.cuisine}|${c.category}`));
  assert.equal(uniqueCells.size, cells.length, `存在重复的菜系×品类格子（去重后 ${uniqueCells.size} / 共 ${cells.length}）`);
  assert.ok(cells.length >= 400, `格子数 ${cells.length} 明显少于分类体系规模`);
  for (const c of cells) {
    assert.ok(c.category, '格子需含 category');
    assert.equal(typeof c.target, 'number');
    assert.equal(typeof c.actual, 'number');
    assert.ok(Array.isArray(c.ids));
  }
  const totalTarget = cells.reduce((a, c) => a + c.target, 0);
  assert.ok(totalTarget >= 3000, `总目标 ${totalTarget} 应不少于 3000`);
  assert.equal(progress.totals.target, totalTarget);
});
