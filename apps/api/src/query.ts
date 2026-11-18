/**
 * 查询层：把 URL 查询参数翻译成 Drizzle 条件，并组装稳定的响应结构。
 * 约定：所有列表接口返回 Paginated<T>，字段在所有端保持一致。
 */
import { and, asc, desc, eq, sql, type SQL } from 'drizzle-orm';
import { recipes, type Db } from '@caipu/db';
import type { Paginated, RecipeListQuery, RecipeSummary } from '@caipu/shared';
import { expandQuery } from './search.js';

export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;

const concat = (table: string, column: string, alias: string) =>
  sql<string | null>`(select group_concat(${sql.raw(column)}, ',') from ${sql.raw(table)} x where x.recipe_id = ${recipes.id})`.as(alias);

const summarySelect = {
  id: recipes.id,
  nameZh: recipes.nameZh,
  nameEn: recipes.nameEn,
  nameOriginal: recipes.nameOriginal,
  region: recipes.region,
  cuisine: recipes.cuisine,
  difficulty: recipes.difficulty,
  totalMin: recipes.totalMin,
  servings: recipes.servings,
  imageUrl: recipes.imageUrl,
  status: recipes.status,
  categories: concat('recipe_categories', 'category', 'categories'),
  flavors: concat('recipe_flavors', 'flavor', 'flavors'),
  dietTags: concat('recipe_diet_tags', 'diet_tag', 'diet_tags'),
  allergens: concat('recipe_allergens', 'allergen', 'allergens')
};

type SummaryRow = {
  id: string;
  nameZh: string;
  nameEn: string;
  nameOriginal: string | null;
  region: string;
  cuisine: string;
  difficulty: number;
  totalMin: number;
  servings: number;
  imageUrl: string | null;
  status: string;
  categories: string | null;
  flavors: string | null;
  dietTags: string | null;
  allergens: string | null;
};

const split = (v: string | null): string[] => (v ? v.split(',').filter(Boolean) : []);

export function toSummary(r: SummaryRow): RecipeSummary {
  return {
    id: r.id,
    name: { zh: r.nameZh, en: r.nameEn, ...(r.nameOriginal ? { original: r.nameOriginal } : {}) },
    cuisine: { region: r.region as 'cn' | 'intl', style: r.cuisine },
    category: split(r.categories).sort(),
    difficulty: r.difficulty as RecipeSummary['difficulty'],
    total_min: r.totalMin,
    servings: r.servings,
    flavor: split(r.flavors).sort(),
    diet_tags: split(r.dietTags).sort(),
    allergens: split(r.allergens).sort(),
    image_url: r.imageUrl,
    status: r.status as RecipeSummary['status']
  };
}

export interface NormalizedQuery {
  page: number;
  pageSize: number;
  conditions: SQL[];
  sort: string;
  q: string | null;
}

export function normalizeQuery(input: RecipeListQuery & { allergen?: string; ingredientKey?: string }): NormalizedQuery {
  const page = Math.max(1, Number(input.page) || 1);
  const pageSize = Math.min(MAX_PAGE_SIZE, Math.max(1, Number(input.pageSize) || DEFAULT_PAGE_SIZE));
  const conditions: SQL[] = [];

  if (input.region === 'cn' || input.region === 'intl') conditions.push(eq(recipes.region, input.region));
  if (input.cuisine) conditions.push(eq(recipes.cuisine, String(input.cuisine)));
  if (input.difficulty) conditions.push(eq(recipes.difficulty, Number(input.difficulty)));
  if (input.maxTime) conditions.push(sql`${recipes.totalMin} <= ${Number(input.maxTime)}`);
  if (input.status) conditions.push(eq(recipes.status, String(input.status)));
  else conditions.push(eq(recipes.status, 'published'));

  const catList = toArray(input.category);
  if (catList.length) {
    conditions.push(
      sql`exists (select 1 from recipe_categories rc where rc.recipe_id = ${recipes.id} and rc.category in (${sql.join(catList.map((c) => sql`${c}`), sql`, `)}))`
    );
  }
  const flavorList = toArray(input.flavor);
  if (flavorList.length) {
    conditions.push(
      sql`exists (select 1 from recipe_flavors rf where rf.recipe_id = ${recipes.id} and rf.flavor in (${sql.join(flavorList.map((c) => sql`${c}`), sql`, `)}))`
    );
  }
  const dietList = toArray(input.diet);
  if (dietList.length) {
    for (const d of dietList) {
      conditions.push(sql`exists (select 1 from recipe_diet_tags rd where rd.recipe_id = ${recipes.id} and rd.diet_tag = ${d})`);
    }
  }
  if (input.allergen) {
    conditions.push(
      sql`not exists (select 1 from recipe_allergens ra where ra.recipe_id = ${recipes.id} and ra.allergen = ${String(input.allergen)})`
    );
  }
  const ingList = toArray(input.ingredient);
  if (ingList.length) {
    for (const name of ingList) {
      conditions.push(
        sql`exists (select 1 from recipe_ingredients ri where ri.recipe_id = ${recipes.id} and (ri.name = ${name} or ri.ing_key = ${name}))`
      );
    }
  }
  if (input.ingredientKey) {
    conditions.push(
      sql`exists (select 1 from recipe_ingredients ri where ri.recipe_id = ${recipes.id} and ri.ing_key = ${String(input.ingredientKey)})`
    );
  }

  const q = (input.q ?? '').trim();
  if (q) {
    // 同义词 + 拼音扩展：任何一个变体命中即可召回，排序时再按原始词的匹配位置加权
    const expansion = expandQuery(q);
    const likes: SQL[] = [];
    for (const term of expansion.terms) {
      const like = `%${term.toLowerCase()}%`;
      likes.push(
        sql`(${recipes.searchText} like ${like} or lower(${recipes.nameZh}) like ${like}
          or lower(${recipes.nameEn}) like ${like} or lower(${recipes.nameOriginal}) like ${like}
          or lower(${recipes.id}) like ${like})`
      );
    }
    for (const py of [...expansion.fullPinyin, ...expansion.initials]) {
      const like = `%${py}%`;
      likes.push(sql`(lower(${recipes.nameEn}) like ${like} or lower(${recipes.id}) like ${like})`);
    }
    if (likes.length) conditions.push(sql`(${sql.join(likes, sql` or `)})`);
  }

  return { page, pageSize, conditions, sort: String(input.sort ?? (q ? 'relevance' : 'newest')), q: q || null };
}

function toArray(v: unknown): string[] {
  if (v === undefined || v === null || v === '') return [];
  if (Array.isArray(v)) return v.map(String).filter(Boolean);
  return String(v).split(',').map((s) => s.trim()).filter(Boolean);
}

function orderBy(sort: string, q: string | null) {
  switch (sort) {
    case 'quickest':
      return [asc(recipes.totalMin), asc(recipes.id)];
    case 'easiest':
      return [asc(recipes.difficulty), asc(recipes.id)];
    case 'name':
      return [asc(recipes.nameZh), asc(recipes.id)];
    case 'relevance': {
      if (!q) return [desc(recipes.updatedAt), asc(recipes.id)];
      const term = q.toLowerCase();
      const expansion = expandQuery(q);
      const py = [...expansion.fullPinyin, ...expansion.initials];
      // 分级：菜名命中 > 拼音/英文/slug 命中 > 全文命中；同级按用时短排序，贴合「找快手菜」的真实诉求
      const pyScore = py.length
        ? sql`case when lower(${recipes.id}) like ${py[0] + '%'} then 5 when lower(${recipes.nameEn}) like ${'%' + py[0] + '%'} then 6 else 7 end`
        : sql`7`;
      const score = sql`case
        when lower(${recipes.nameZh}) = ${term} then 0
        when lower(${recipes.nameZh}) like ${term + '%'} then 1
        when lower(${recipes.nameEn}) = ${term} then 2
        when lower(${recipes.nameEn}) like ${term + '%'} then 3
        when lower(${recipes.nameZh}) like ${'%' + term + '%'} then 4
        else ${pyScore} end`;
      return [asc(score), asc(recipes.totalMin), asc(recipes.id)];
    }
    case 'newest':
    default:
      return [desc(recipes.updatedAt), asc(recipes.id)];
  }
}

export function listRecipes(db: Db, input: RecipeListQuery & { allergen?: string; ingredientKey?: string }): Paginated<RecipeSummary> {
  const nq = normalizeQuery(input);
  const where = nq.conditions.length ? and(...nq.conditions) : undefined;

  const totalRow = db.db
    .select({ c: sql<number>`count(*)` })
    .from(recipes)
    .where(where)
    .all() as Array<{ c: number }>;
  const total = Number(totalRow[0]?.c ?? 0);

  const rows = db.db
    .select(summarySelect)
    .from(recipes)
    .where(where)
    .orderBy(...orderBy(nq.sort, nq.q))
    .limit(nq.pageSize)
    .offset((nq.page - 1) * nq.pageSize)
    .all() as SummaryRow[];

  const totalPages = Math.max(1, Math.ceil(total / nq.pageSize));
  return {
    items: rows.map(toSummary),
    page: nq.page,
    pageSize: nq.pageSize,
    total,
    totalPages,
    hasNext: nq.page < totalPages
  };
}

export function getRecipeById(db: Db, id: string) {
  const row = db.db.select({ data: recipes.data }).from(recipes).where(eq(recipes.id, id)).all() as Array<{ data: string }>;
  if (!row.length) return null;
  return JSON.parse(row[0].data);
}

export function getSummariesByIds(db: Db, ids: string[]): RecipeSummary[] {
  if (!ids.length) return [];
  const rows = db.db
    .select(summarySelect)
    .from(recipes)
    .where(sql`${recipes.id} in (${sql.join(ids.map((i) => sql`${i}`), sql`, `)})`)
    .all() as SummaryRow[];
  const map = new Map(rows.map((r) => [r.id, toSummary(r)]));
  return ids.map((i) => map.get(i)).filter(Boolean) as RecipeSummary[];
}

export function randomRecipes(db: Db, count: number, opts: { cuisine?: string; category?: string; diet?: string } = {}) {
  const conditions: SQL[] = [eq(recipes.status, 'published')];
  if (opts.cuisine) conditions.push(eq(recipes.cuisine, opts.cuisine));
  if (opts.category) {
    conditions.push(
      sql`exists (select 1 from recipe_categories rc where rc.recipe_id = ${recipes.id} and rc.category = ${opts.category})`
    );
  }
  if (opts.diet) {
    conditions.push(
      sql`exists (select 1 from recipe_diet_tags rd where rd.recipe_id = ${recipes.id} and rd.diet_tag = ${opts.diet})`
    );
  }
  const rows = db.db
    .select(summarySelect)
    .from(recipes)
    .where(and(...conditions))
    .orderBy(sql`random()`)
    .limit(Math.min(50, Math.max(1, count)))
    .all() as SummaryRow[];
  return rows.map(toSummary);
}
