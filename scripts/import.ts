/**
 * 菜谱导入脚本：data/recipes/**\/*.json → SQLite
 * 用法：tsx scripts/import.ts [--reset] [--allow-invalid]
 * 幂等：默认在同一事务内清空菜谱相关表后全量重建；--reset 会同时重建基础表。
 */
import fs from 'node:fs';
import path from 'node:path';
import { createDb, resolveDbPath, REPO_ROOT } from '../packages/db/src/index.js';
import { walkRecipeFiles, loadTaxonomy, loadIngredients, loadSchema, buildNameIndex, relPath } from './lib/loaders.mjs';
import { validate } from './lib/schema-lite.mjs';
import { pinyin } from 'pinyin-pro';
import { toGrams } from './lib/rules.mjs';

const argv = process.argv.slice(2);
const allowInvalid = argv.includes('--allow-invalid');

const taxonomy = loadTaxonomy();
const dict = loadIngredients();
const schema = loadSchema();
const nameIndex = buildNameIndex(dict);
const cuisineZh = new Map(taxonomy.cuisines.map((c: any) => [c.slug, c.zh]));
const catZh = new Map(taxonomy.categories.map((c: any) => [c.slug, c.zh]));

const dbPath = resolveDbPath();
const { sqlite } = createDb(dbPath);

const startedAt = new Date().toISOString();
const runRow = sqlite
  .prepare('INSERT INTO import_runs (started_at, note) VALUES (?, ?)')
  .run(startedAt, `import from ${relPath(REPO_ROOT)}`);
const runId = Number(runRow.lastInsertRowid);

const files = walkRecipeFiles();
let seen = 0;
let imported = 0;
let skipped = 0;
const problems: string[] = [];

const stmts = {
  recipe: sqlite.prepare(`
    INSERT INTO recipes (id, name_zh, name_en, name_original, region, cuisine, difficulty,
      prep_min, cook_min, total_min, servings, status, image_url, image_credit, calories_kcal,
      content_version, created_at, updated_at, search_text, data)
    VALUES (@id, @nameZh, @nameEn, @nameOriginal, @region, @cuisine, @difficulty,
      @prepMin, @cookMin, @totalMin, @servings, @status, @imageUrl, @imageCredit, @caloriesKcal,
      @contentVersion, @createdAt, @updatedAt, @searchText, @data)
  `),
  category: sqlite.prepare('INSERT OR IGNORE INTO recipe_categories (recipe_id, category) VALUES (?, ?)'),
  flavor: sqlite.prepare('INSERT OR IGNORE INTO recipe_flavors (recipe_id, flavor) VALUES (?, ?)'),
  diet: sqlite.prepare('INSERT OR IGNORE INTO recipe_diet_tags (recipe_id, diet_tag) VALUES (?, ?)'),
  allergen: sqlite.prepare('INSERT OR IGNORE INTO recipe_allergens (recipe_id, allergen) VALUES (?, ?)'),
  ingredient: sqlite.prepare(`
    INSERT INTO recipe_ingredients (recipe_id, seq, group_name, name, name_en, ing_key, amount, unit, note, substitute, optional, grams)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
  `),
  step: sqlite.prepare(`
    INSERT INTO recipe_steps (recipe_id, n, text, time_min, heat, tip, visual_cue)
    VALUES (?,?,?,?,?,?,?)
  `),
  equipment: sqlite.prepare('INSERT OR IGNORE INTO recipe_equipment (recipe_id, equipment) VALUES (?, ?)'),
  related: sqlite.prepare('INSERT OR IGNORE INTO recipe_related (recipe_id, related_id) VALUES (?, ?)')
};

function buildSearchText(d: any): string {
  const parts: string[] = [];
  parts.push(d.name?.zh ?? '', d.name?.en ?? '', d.name?.original ?? '');
  // 拼音索引：用户常用「mapo」「mpdf」这类输入，中文名转全拼与首字母后并入检索文本
  const zhName = String(d.name?.zh ?? '');
  if (zhName) {
    parts.push(pinyin(zhName, { toneType: 'none', type: 'array' }).join(''));
    parts.push(pinyin(zhName, { pattern: 'first', toneType: 'none', type: 'array' }).join(''));
  }
  parts.push(cuisineZh.get(d.cuisine?.style) ?? d.cuisine?.style ?? '');
  for (const c of d.category ?? []) parts.push(catZh.get(c) ?? c, c);
  parts.push(...(d.flavor ?? []), ...(d.diet_tags ?? []), ...(d.tags ?? []));
  for (const g of d.ingredients ?? []) for (const it of g.items ?? []) parts.push(it.name ?? '', it.name_en ?? '');
  parts.push(d.serving_suggestion ?? '', d.origin_note ?? '');
  return parts.join(' ').toLowerCase().replace(/\s+/g, ' ').trim();
}

const importAll = sqlite.transaction(() => {
  for (const t of ['recipe_related', 'recipe_equipment', 'recipe_steps', 'recipe_ingredients',
    'recipe_allergens', 'recipe_diet_tags', 'recipe_flavors', 'recipe_categories', 'recipes']) {
    sqlite.exec(`DELETE FROM ${t}`);
  }

  for (const f of files) {
    seen++;
    let d: any;
    try {
      d = JSON.parse(fs.readFileSync(f, 'utf8').replace(/^\uFEFF/, ''));
    } catch (e: any) {
      problems.push(`${relPath(f)}: JSON 解析失败 ${e.message}`);
      skipped++;
      continue;
    }
    const errs = validate(schema, d);
    if (errs.length && !allowInvalid) {
      problems.push(`${relPath(f)}: schema 校验失败（${errs.length} 项）${errs[0]}`);
      skipped++;
      continue;
    }

    try {
      stmts.recipe.run({
        id: d.id,
        nameZh: d.name.zh,
        nameEn: d.name.en,
        nameOriginal: d.name.original ?? null,
        region: d.cuisine.region,
        cuisine: d.cuisine.style,
        difficulty: d.difficulty,
        prepMin: d.time.prep_min,
        cookMin: d.time.cook_min,
        totalMin: d.time.total_min,
        servings: d.servings,
        status: d.status,
        imageUrl: d.image_url ?? null,
        imageCredit: d.image_credit ?? null,
        caloriesKcal: d.nutrition_estimate?.calories_kcal ?? null,
        contentVersion: d.content_version ?? 1,
        createdAt: d.created_at,
        updatedAt: d.updated_at,
        searchText: buildSearchText(d),
        data: JSON.stringify(d)
      });
      for (const c of d.category ?? []) stmts.category.run(d.id, c);
      for (const v of d.flavor ?? []) stmts.flavor.run(d.id, v);
      for (const v of d.diet_tags ?? []) stmts.diet.run(d.id, v);
      for (const v of d.allergens ?? []) stmts.allergen.run(d.id, v);
      for (const v of d.equipment ?? []) stmts.equipment.run(d.id, v);
      for (const v of d.related_ids ?? []) stmts.related.run(d.id, v);

      let seq = 0;
      for (const g of d.ingredients ?? []) {
        for (const it of g.items ?? []) {
          const entry = nameIndex.get(it.name);
          stmts.ingredient.run(
            d.id, ++seq, g.group, it.name, it.name_en ?? entry?.en ?? null,
            entry?.key ?? null, Number(it.amount) || 0, it.unit,
            it.note ?? null, it.substitute ?? null, it.optional ? 1 : 0,
            toGrams(Number(it.amount) || 0, it.unit, entry)
          );
        }
      }
      for (const s of d.steps ?? []) {
        stmts.step.run(d.id, s.n, s.text, s.time_min ?? 0, s.heat ?? '无火', s.tip ?? '', s.visual_cue ?? '');
      }
      imported++;
    } catch (e: any) {
      problems.push(`${relPath(f)}: 写入失败 ${e.message}`);
      skipped++;
    }
  }
});

importAll();

const finishedAt = new Date().toISOString();
sqlite
  .prepare('UPDATE import_runs SET finished_at=?, files_seen=?, files_imported=?, files_failed=? WHERE id=?')
  .run(finishedAt, seen, imported, skipped, runId);

const stats = {
  files: seen,
  imported,
  skipped,
  recipes: (sqlite.prepare('SELECT COUNT(*) c FROM recipes').get() as any).c,
  ingredients: (sqlite.prepare('SELECT COUNT(*) c FROM recipe_ingredients').get() as any).c,
  steps: (sqlite.prepare('SELECT COUNT(*) c FROM recipe_steps').get() as any).c
};

console.log(`导入完成：${JSON.stringify(stats)}`);
if (problems.length) {
  console.log(`\n跳过/异常 ${problems.length} 项：`);
  for (const p of problems.slice(0, 30)) console.log('  - ' + p);
  if (problems.length > 30) console.log(`  ... 其余 ${problems.length - 30} 项省略`);
}
sqlite.close();
process.exit(skipped > 0 && !allowInvalid ? 1 : 0);
