import type { FastifyInstance } from 'fastify';
import { sql, eq } from 'drizzle-orm';
import { ingredientsDict, type Db } from '@caipu/db';
import { getSummariesByIds } from '../query.js';

export async function ingredientRoutes(app: FastifyInstance, opts: { db: Db }) {
  const { db } = opts;

  app.get('/ingredients', async (req) => {
    const q = req.query as { q?: string; category?: string; page?: string; pageSize?: string };
    const page = Math.max(1, Number(q.page) || 1);
    const pageSize = Math.min(200, Math.max(1, Number(q.pageSize) || 60));
    const keyword = (q.q ?? '').trim();

    const usage = new Map(
      (db.sqlite
        .prepare(
          `SELECT ri.ing_key AS k, COUNT(DISTINCT ri.recipe_id) AS c
           FROM recipe_ingredients ri JOIN recipes r ON r.id = ri.recipe_id
           WHERE r.status='published' AND ri.ing_key IS NOT NULL GROUP BY ri.ing_key`
        )
        .all() as Array<{ k: string; c: number }>).map((r) => [r.k, r.c])
    );

    let rows = db.db.select().from(ingredientsDict).all() as Array<{
      key: string; zh: string; en: string; aliases: string; allergens: string; category: string;
    }>;

    if (q.category) rows = rows.filter((r) => r.category === q.category);
    if (keyword) {
      const k = keyword.toLowerCase();
      rows = rows.filter(
        (r) =>
          r.zh.includes(keyword) ||
          r.en.toLowerCase().includes(k) ||
          (JSON.parse(r.aliases) as string[]).some((a) => a.includes(keyword))
      );
    }

    rows.sort((a, b) => (usage.get(b.key) ?? 0) - (usage.get(a.key) ?? 0) || a.zh.localeCompare(b.zh, 'zh'));

    const total = rows.length;
    const slice = rows.slice((page - 1) * pageSize, page * pageSize);
    return {
      items: slice.map((r) => ({
        key: r.key,
        zh: r.zh,
        en: r.en,
        aliases: JSON.parse(r.aliases),
        allergens: JSON.parse(r.allergens),
        category: r.category,
        recipeCount: usage.get(r.key) ?? 0
      })),
      page,
      pageSize,
      total,
      totalPages: Math.max(1, Math.ceil(total / pageSize)),
      hasNext: page * pageSize < total
    };
  });

  app.get('/ingredients/:key', async (req, reply) => {
    const { key } = req.params as { key: string };
    const row = db.db.select().from(ingredientsDict).where(eq(ingredientsDict.key, key)).all()[0] as
      | { key: string; zh: string; en: string; aliases: string; allergens: string; category: string }
      | undefined;
    if (!row) return reply.code(404).send({ error: 'not_found', message: `食材 ${key} 不存在` });

    const ids = (db.sqlite
      .prepare(
        `SELECT DISTINCT ri.recipe_id AS id FROM recipe_ingredients ri
         JOIN recipes r ON r.id = ri.recipe_id
         WHERE r.status='published' AND (ri.ing_key = ? OR ri.name = ?)
         ORDER BY r.updated_at DESC LIMIT 100`
      )
      .all(key, row.zh) as Array<{ id: string }>).map((r) => r.id);

    return {
      key: row.key,
      zh: row.zh,
      en: row.en,
      aliases: JSON.parse(row.aliases),
      allergens: JSON.parse(row.allergens),
      category: row.category,
      recipeCount: ids.length,
      recipes: getSummariesByIds(db, ids)
    };
  });

  app.get('/ingredients/:key/recipes', async (req) => {
    const { key } = req.params as { key: string };
    const q = req.query as { page?: string; pageSize?: string };
    const page = Math.max(1, Number(q.page) || 1);
    const pageSize = Math.min(100, Math.max(1, Number(q.pageSize) || 20));

    const totalRow = db.sqlite
      .prepare(
        `SELECT COUNT(DISTINCT ri.recipe_id) AS c FROM recipe_ingredients ri
         JOIN recipes r ON r.id = ri.recipe_id WHERE r.status='published' AND ri.ing_key = ?`
      )
      .get(key) as { c: number };
    const ids = (db.sqlite
      .prepare(
        `SELECT DISTINCT ri.recipe_id AS id FROM recipe_ingredients ri
         JOIN recipes r ON r.id = ri.recipe_id
         WHERE r.status='published' AND ri.ing_key = ?
         ORDER BY r.updated_at DESC LIMIT ? OFFSET ?`
      )
      .all(key, pageSize, (page - 1) * pageSize) as Array<{ id: string }>).map((r) => r.id);

    const total = totalRow?.c ?? 0;
    const totalPages = Math.max(1, Math.ceil(total / pageSize));
    return {
      items: getSummariesByIds(db, ids),
      page,
      pageSize,
      total,
      totalPages,
      hasNext: page < totalPages
    };
  });
}
