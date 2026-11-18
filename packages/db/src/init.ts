/**
 * 初始化数据库：建表 + 导入分类体系与食材词典
 * 用法：tsx packages/db/src/init.ts [--reset]
 */
import fs from 'node:fs';
import path from 'node:path';
import { createDb, resolveDbPath, REPO_ROOT } from './index.js';
import { cuisines, categories, ingredientsDict } from './schema.js';

const DDL = `
CREATE TABLE IF NOT EXISTS cuisines (
  slug TEXT PRIMARY KEY,
  region TEXT NOT NULL,
  zh TEXT NOT NULL,
  en TEXT NOT NULL,
  tier TEXT NOT NULL,
  intro TEXT NOT NULL DEFAULT '',
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS categories (
  slug TEXT PRIMARY KEY,
  zh TEXT NOT NULL,
  en TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ingredients_dict (
  key TEXT PRIMARY KEY,
  zh TEXT NOT NULL,
  en TEXT NOT NULL,
  aliases TEXT NOT NULL DEFAULT '[]',
  allergens TEXT NOT NULL DEFAULT '[]',
  category TEXT NOT NULL DEFAULT 'other'
);
CREATE INDEX IF NOT EXISTS idx_ingredients_zh ON ingredients_dict(zh);

CREATE TABLE IF NOT EXISTS recipes (
  id TEXT PRIMARY KEY,
  name_zh TEXT NOT NULL,
  name_en TEXT NOT NULL,
  name_original TEXT,
  region TEXT NOT NULL,
  cuisine TEXT NOT NULL,
  difficulty INTEGER NOT NULL,
  prep_min INTEGER NOT NULL,
  cook_min INTEGER NOT NULL,
  total_min INTEGER NOT NULL,
  servings INTEGER NOT NULL,
  status TEXT NOT NULL,
  image_url TEXT,
  image_credit TEXT,
  calories_kcal INTEGER,
  content_version INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  search_text TEXT NOT NULL DEFAULT '',
  data TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX IF NOT EXISTS idx_recipes_region ON recipes(region);
CREATE INDEX IF NOT EXISTS idx_recipes_difficulty ON recipes(difficulty);
CREATE INDEX IF NOT EXISTS idx_recipes_total_min ON recipes(total_min);
CREATE INDEX IF NOT EXISTS idx_recipes_status ON recipes(status);
CREATE INDEX IF NOT EXISTS idx_recipes_search ON recipes(search_text);

CREATE TABLE IF NOT EXISTS recipe_categories (
  recipe_id TEXT NOT NULL,
  category TEXT NOT NULL,
  PRIMARY KEY (recipe_id, category)
);
CREATE INDEX IF NOT EXISTS idx_rc_category ON recipe_categories(category);

CREATE TABLE IF NOT EXISTS recipe_flavors (
  recipe_id TEXT NOT NULL,
  flavor TEXT NOT NULL,
  PRIMARY KEY (recipe_id, flavor)
);
CREATE INDEX IF NOT EXISTS idx_rf_flavor ON recipe_flavors(flavor);

CREATE TABLE IF NOT EXISTS recipe_diet_tags (
  recipe_id TEXT NOT NULL,
  diet_tag TEXT NOT NULL,
  PRIMARY KEY (recipe_id, diet_tag)
);
CREATE INDEX IF NOT EXISTS idx_rdt_tag ON recipe_diet_tags(diet_tag);

CREATE TABLE IF NOT EXISTS recipe_allergens (
  recipe_id TEXT NOT NULL,
  allergen TEXT NOT NULL,
  PRIMARY KEY (recipe_id, allergen)
);
CREATE INDEX IF NOT EXISTS idx_ra_allergen ON recipe_allergens(allergen);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
  recipe_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  group_name TEXT NOT NULL,
  name TEXT NOT NULL,
  name_en TEXT,
  ing_key TEXT,
  amount REAL NOT NULL,
  unit TEXT NOT NULL,
  note TEXT,
  substitute TEXT,
  optional INTEGER NOT NULL DEFAULT 0,
  grams REAL NOT NULL DEFAULT 0,
  PRIMARY KEY (recipe_id, seq)
);
CREATE INDEX IF NOT EXISTS idx_ri_name ON recipe_ingredients(name);
CREATE INDEX IF NOT EXISTS idx_ri_key ON recipe_ingredients(ing_key);

CREATE TABLE IF NOT EXISTS recipe_steps (
  recipe_id TEXT NOT NULL,
  n INTEGER NOT NULL,
  text TEXT NOT NULL,
  time_min INTEGER NOT NULL DEFAULT 0,
  heat TEXT NOT NULL DEFAULT '无火',
  tip TEXT NOT NULL DEFAULT '',
  visual_cue TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (recipe_id, n)
);

CREATE TABLE IF NOT EXISTS recipe_equipment (
  recipe_id TEXT NOT NULL,
  equipment TEXT NOT NULL,
  PRIMARY KEY (recipe_id, equipment)
);

CREATE TABLE IF NOT EXISTS recipe_related (
  recipe_id TEXT NOT NULL,
  related_id TEXT NOT NULL,
  PRIMARY KEY (recipe_id, related_id)
);

CREATE TABLE IF NOT EXISTS import_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  files_seen INTEGER NOT NULL DEFAULT 0,
  files_imported INTEGER NOT NULL DEFAULT 0,
  files_failed INTEGER NOT NULL DEFAULT 0,
  note TEXT
);
`;

function readJson(p: string) {
  return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
}

function main() {
  const reset = process.argv.includes('--reset');
  const dbPath = resolveDbPath();
  if (reset && fs.existsSync(dbPath)) {
    for (const ext of ['', '-wal', '-shm']) {
      const f = dbPath + ext;
      if (fs.existsSync(f)) fs.rmSync(f);
    }
    console.log(`已删除旧数据库：${dbPath}`);
  }

  const { sqlite } = createDb(dbPath);
  sqlite.exec(DDL);
  console.log(`建表完成：${dbPath}`);

  const taxonomy = readJson(path.join(REPO_ROOT, 'data', 'taxonomy.json'));
  const dict = readJson(path.join(REPO_ROOT, 'data', 'ingredients.json'));

  const insertCuisine = sqlite.prepare(
    `INSERT INTO cuisines (slug, region, zh, en, tier, intro, sort_order) VALUES (?,?,?,?,?,?,?)
     ON CONFLICT(slug) DO UPDATE SET region=excluded.region, zh=excluded.zh, en=excluded.en,
     tier=excluded.tier, intro=excluded.intro, sort_order=excluded.sort_order`
  );
  const insertCategory = sqlite.prepare(
    `INSERT INTO categories (slug, zh, en, description, sort_order) VALUES (?,?,?,?,?)
     ON CONFLICT(slug) DO UPDATE SET zh=excluded.zh, en=excluded.en,
     description=excluded.description, sort_order=excluded.sort_order`
  );
  const insertIngredient = sqlite.prepare(
    `INSERT INTO ingredients_dict (key, zh, en, aliases, allergens, category) VALUES (?,?,?,?,?,?)
     ON CONFLICT(key) DO UPDATE SET zh=excluded.zh, en=excluded.en, aliases=excluded.aliases,
     allergens=excluded.allergens, category=excluded.category`
  );

  const tx = sqlite.transaction(() => {
    taxonomy.cuisines.forEach((c: any, i: number) => {
      insertCuisine.run(c.slug, c.region, c.zh, c.en, c.tier, c.intro ?? '', i);
    });
    taxonomy.categories.forEach((c: any, i: number) => {
      insertCategory.run(c.slug, c.zh, c.en, c.desc ?? '', i);
    });
    for (const it of dict.items) {
      insertIngredient.run(it.key, it.zh, it.en, JSON.stringify(it.aliases ?? []), JSON.stringify(it.allergens ?? []), it.category ?? 'other');
    }
  });
  tx();

  const counts = {
    cuisines: (sqlite.prepare('SELECT COUNT(*) c FROM cuisines').get() as any).c,
    categories: (sqlite.prepare('SELECT COUNT(*) c FROM categories').get() as any).c,
    ingredients: (sqlite.prepare('SELECT COUNT(*) c FROM ingredients_dict').get() as any).c
  };
  console.log(`基础数据导入完成：${JSON.stringify(counts)}`);
  sqlite.close();
}

main();
