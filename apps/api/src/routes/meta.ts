import type { FastifyInstance } from 'fastify';
import fs from 'node:fs';
import path from 'node:path';
import { sql, eq, asc } from 'drizzle-orm';
import { REPO_ROOT, cuisines, categories, recipes, ingredientsDict, type Db } from '@caipu/db';

const PUBLISHED = sql`${recipes.status} = 'published'`;

/**
 * 风味 / 饮食标签 / 过敏原的完整可选值来自 taxonomy.json（唯一真相），
 * 不能只从数据库出现过的值里推导——新库为空时筛选项会全部消失。
 */
type TagItem = { slug: string; zh: string; en?: string };
const taxonomy = JSON.parse(
  fs.readFileSync(path.join(REPO_ROOT, 'data', 'taxonomy.json'), 'utf8').replace(/^\uFEFF/, '')
) as { flavors: TagItem[]; dietTags: TagItem[]; allergens: TagItem[]; regions: Array<{ slug: string; zh: string }> };

export async function metaRoutes(app: FastifyInstance, opts: { db: Db }) {
  const { db } = opts;

  const countBy = (sqlText: string) =>
    db.sqlite.prepare(sqlText).all() as Array<{ k: string; c: number }>;

  const cuisineCounts = new Map(countBy('SELECT cuisine AS k, COUNT(*) AS c FROM recipes GROUP BY cuisine').map((r) => [r.k, r.c]));
  const categoryCounts = new Map(
    countBy(
      "SELECT rc.category AS k, COUNT(*) AS c FROM recipe_categories rc JOIN recipes r ON r.id = rc.recipe_id WHERE r.status = 'published' GROUP BY rc.category"
    ).map((r) => [r.k, r.c])
  );
  const flavorCounts = new Map(
    countBy(
      "SELECT rf.flavor AS k, COUNT(*) AS c FROM recipe_flavors rf JOIN recipes r ON r.id = rf.recipe_id WHERE r.status = 'published' GROUP BY rf.flavor"
    ).map((r) => [r.k, r.c])
  );
  const dietCounts = new Map(
    countBy(
      "SELECT rd.diet_tag AS k, COUNT(*) AS c FROM recipe_diet_tags rd JOIN recipes r ON r.id = rd.recipe_id WHERE r.status = 'published' GROUP BY rd.diet_tag"
    ).map((r) => [r.k, r.c])
  );
  const allergenCounts = new Map(
    countBy(
      "SELECT ra.allergen AS k, COUNT(*) AS c FROM recipe_allergens ra JOIN recipes r ON r.id = ra.recipe_id WHERE r.status = 'published' GROUP BY ra.allergen"
    ).map((r) => [r.k, r.c])
  );

  const cuisineRows = db.db
    .select()
    .from(cuisines)
    .orderBy(asc(cuisines.sortOrder))
    .all();
  const categoryRows = db.db
    .select()
    .from(categories)
    .orderBy(asc(categories.sortOrder))
    .all();

  app.get('/meta', async () => {
    const total = db.db.select({ c: sql<number>`count(*)` }).from(recipes).where(eq(recipes.status, 'published')).all() as Array<{ c: number }>;
    const counts = {
      recipes: Number(total[0]?.c ?? 0),
      cuisines: cuisineRows.length,
      categories: categoryRows.length,
      ingredients:
        (db.db.select({ c: sql<number>`count(*)` }).from(ingredientsDict).all() as Array<{ c: number }>)[0]?.c ?? 0
    };
    return {
      version: 'v1',
      schemaVersion: 1,
      defaultLocale: 'zh',
      locales: ['zh', 'en'],
      counts,
      // stats 为旧字段，保留以兼容早期客户端
      stats: counts,
      regions: taxonomy.regions.map((r) => ({ value: r.slug, label: r.zh })),
      difficulties: [1, 2, 3, 4, 5].map((d) => ({ value: d, label: String(d) })),
      flavors: taxonomy.flavors.map((f) => ({ value: f.slug, label: f.zh })),
      dietTags: taxonomy.dietTags.map((d) => ({ value: d.slug, label: d.zh })),
      allergens: taxonomy.allergens.map((a) => ({ value: a.slug, label: a.zh })),
      cuisines: cuisineRows.map((c) => ({ ...c, count: cuisineCounts.get(c.slug) ?? 0 })),
      categories: categoryRows.map((c) => ({ ...c, count: categoryCounts.get(c.slug) ?? 0 }))
    };
  });

  app.get('/cuisines', async (req) => {
    const region = (req.query as { region?: string })?.region;
    const list = region ? cuisineRows.filter((c) => c.region === region) : cuisineRows;
    return {
      items: list.map((c) => ({ ...c, count: cuisineCounts.get(c.slug) ?? 0 })),
      total: list.length
    };
  });

  app.get('/cuisines/:slug', async (req, reply) => {
    const { slug } = req.params as { slug: string };
    const row = cuisineRows.find((c) => c.slug === slug);
    if (!row) return reply.code(404).send({ error: 'not_found', message: `菜系 ${slug} 不存在` });
    const cats = db.sqlite
      .prepare(
        `SELECT rc.category AS slug, COUNT(*) AS count FROM recipe_categories rc
         JOIN recipes r ON r.id = rc.recipe_id WHERE r.cuisine = ? AND r.status='published'
         GROUP BY rc.category ORDER BY count DESC`
      )
      .all(slug) as Array<{ slug: string; count: number }>;
    return { ...row, count: cuisineCounts.get(slug) ?? 0, categories: cats };
  });

  app.get('/categories', async () => ({
    items: categoryRows.map((c) => ({ ...c, count: categoryCounts.get(c.slug) ?? 0 })),
    total: categoryRows.length
  }));

  app.get('/filters', async () => ({
    regions: taxonomy.regions.map((r) => ({ value: r.slug, label: r.zh })),
    cuisines: cuisineRows.map((c) => ({ value: c.slug, label: c.zh, region: c.region, count: cuisineCounts.get(c.slug) ?? 0 })),
    categories: categoryRows.map((c) => ({ value: c.slug, label: c.zh, count: categoryCounts.get(c.slug) ?? 0 })),
    difficulties: [1, 2, 3, 4, 5].map((d) => ({ value: d, label: String(d) })),
    flavors: taxonomy.flavors.map((f) => ({ value: f.slug, label: f.zh, count: flavorCounts.get(f.slug) ?? 0 })),
    dietTags: taxonomy.dietTags.map((d) => ({ value: d.slug, label: d.zh, count: dietCounts.get(d.slug) ?? 0 })),
    allergens: taxonomy.allergens.map((a) => ({ value: a.slug, label: a.zh, count: allergenCounts.get(a.slug) ?? 0 })),
    maxTimeOptions: [15, 30, 45, 60, 120]
  }));
}
