/**
 * 数据库结构（Drizzle ORM / SQLite）
 * 迁移到 PostgreSQL 时仅需替换 driver 与少量类型（text→text、integer→integer、real→double precision）。
 * 与 packages/db/src/init.ts 中的 DDL 严格保持一致。
 */
import { sqliteTable, text, integer, real, primaryKey, index } from 'drizzle-orm/sqlite-core';

export const cuisines = sqliteTable('cuisines', {
  slug: text('slug').primaryKey(),
  region: text('region').notNull(),
  zh: text('zh').notNull(),
  en: text('en').notNull(),
  tier: text('tier').notNull(),
  intro: text('intro').notNull().default(''),
  sortOrder: integer('sort_order').notNull().default(0)
});

export const categories = sqliteTable('categories', {
  slug: text('slug').primaryKey(),
  zh: text('zh').notNull(),
  en: text('en').notNull(),
  description: text('description').notNull().default(''),
  sortOrder: integer('sort_order').notNull().default(0)
});

export const ingredientsDict = sqliteTable(
  'ingredients_dict',
  {
    key: text('key').primaryKey(),
    zh: text('zh').notNull(),
    en: text('en').notNull(),
    aliases: text('aliases').notNull().default('[]'),
    allergens: text('allergens').notNull().default('[]'),
    category: text('category').notNull().default('other')
  },
  (t) => ({
    zhIdx: index('idx_ingredients_zh').on(t.zh)
  })
);

export const recipes = sqliteTable(
  'recipes',
  {
    id: text('id').primaryKey(),
    nameZh: text('name_zh').notNull(),
    nameEn: text('name_en').notNull(),
    nameOriginal: text('name_original'),
    region: text('region').notNull(),
    cuisine: text('cuisine').notNull(),
    difficulty: integer('difficulty').notNull(),
    prepMin: integer('prep_min').notNull(),
    cookMin: integer('cook_min').notNull(),
    totalMin: integer('total_min').notNull(),
    servings: integer('servings').notNull(),
    status: text('status').notNull(),
    imageUrl: text('image_url'),
    imageCredit: text('image_credit'),
    caloriesKcal: integer('calories_kcal'),
    contentVersion: integer('content_version').notNull().default(1),
    createdAt: text('created_at').notNull(),
    updatedAt: text('updated_at').notNull(),
    /** 小写检索文本：菜名 + 食材 + 标签 + 菜系 + 简介，供 LIKE 搜索 */
    searchText: text('search_text').notNull().default(''),
    /** 原始完整 JSON，详情接口直接返回，保证字段稳定 */
    data: text('data').notNull()
  },
  (t) => ({
    cuisineIdx: index('idx_recipes_cuisine').on(t.cuisine),
    regionIdx: index('idx_recipes_region').on(t.region),
    difficultyIdx: index('idx_recipes_difficulty').on(t.difficulty),
    totalMinIdx: index('idx_recipes_total_min').on(t.totalMin),
    statusIdx: index('idx_recipes_status').on(t.status),
    searchIdx: index('idx_recipes_search').on(t.searchText)
  })
);

export const recipeCategories = sqliteTable(
  'recipe_categories',
  {
    recipeId: text('recipe_id').notNull(),
    category: text('category').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.category] }),
    catIdx: index('idx_rc_category').on(t.category)
  })
);

export const recipeFlavors = sqliteTable(
  'recipe_flavors',
  {
    recipeId: text('recipe_id').notNull(),
    flavor: text('flavor').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.flavor] }),
    fIdx: index('idx_rf_flavor').on(t.flavor)
  })
);

export const recipeDietTags = sqliteTable(
  'recipe_diet_tags',
  {
    recipeId: text('recipe_id').notNull(),
    dietTag: text('diet_tag').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.dietTag] }),
    dIdx: index('idx_rdt_tag').on(t.dietTag)
  })
);

export const recipeAllergens = sqliteTable(
  'recipe_allergens',
  {
    recipeId: text('recipe_id').notNull(),
    allergen: text('allergen').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.allergen] }),
    aIdx: index('idx_ra_allergen').on(t.allergen)
  })
);

export const recipeIngredients = sqliteTable(
  'recipe_ingredients',
  {
    recipeId: text('recipe_id').notNull(),
    seq: integer('seq').notNull(),
    groupName: text('group_name').notNull(),
    name: text('name').notNull(),
    nameEn: text('name_en'),
    ingKey: text('ing_key'),
    amount: real('amount').notNull(),
    unit: text('unit').notNull(),
    note: text('note'),
    substitute: text('substitute'),
    optional: integer('optional').notNull().default(0),
    grams: real('grams').notNull().default(0)
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.seq] }),
    nameIdx: index('idx_ri_name').on(t.name),
    keyIdx: index('idx_ri_key').on(t.ingKey)
  })
);

export const recipeSteps = sqliteTable(
  'recipe_steps',
  {
    recipeId: text('recipe_id').notNull(),
    n: integer('n').notNull(),
    text: text('text').notNull(),
    timeMin: integer('time_min').notNull().default(0),
    heat: text('heat').notNull().default('无火'),
    tip: text('tip').notNull().default(''),
    visualCue: text('visual_cue').notNull().default('')
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.n] })
  })
);

export const recipeEquipment = sqliteTable(
  'recipe_equipment',
  {
    recipeId: text('recipe_id').notNull(),
    equipment: text('equipment').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.equipment] })
  })
);

export const recipeRelated = sqliteTable(
  'recipe_related',
  {
    recipeId: text('recipe_id').notNull(),
    relatedId: text('related_id').notNull()
  },
  (t) => ({
    pk: primaryKey({ columns: [t.recipeId, t.relatedId] })
  })
);

/** 导入/巡检运行记录，便于回溯 */
export const importRuns = sqliteTable('import_runs', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  startedAt: text('started_at').notNull(),
  finishedAt: text('finished_at'),
  filesSeen: integer('files_seen').notNull().default(0),
  filesImported: integer('files_imported').notNull().default(0),
  filesFailed: integer('files_failed').notNull().default(0),
  note: text('note')
});
