import type { FastifyInstance } from 'fastify';
import type { Db } from '@caipu/db';
import { listRecipes, getRecipeById, getSummariesByIds, randomRecipes } from '../query.js';

export async function recipeRoutes(app: FastifyInstance, opts: { db: Db }) {
  const { db } = opts;

  app.get('/recipes', async (req) => {
    const q = req.query as Record<string, string>;
    return listRecipes(db, {
      page: Number(q.page) || 1,
      pageSize: Number(q.pageSize) || undefined,
      region: q.region as never,
      cuisine: q.cuisine,
      category: q.category as never,
      difficulty: q.difficulty ? (Number(q.difficulty) as never) : undefined,
      flavor: q.flavor,
      diet: q.diet,
      allergen: q.allergen,
      ingredient: q.ingredient,
      q: q.q,
      maxTime: q.maxTime ? Number(q.maxTime) : undefined,
      sort: (q.sort as never) ?? undefined
    });
  });

  app.get('/recipes/random', async (req) => {
    const q = req.query as Record<string, string>;
    // size 与 count 都接受，默认 6 道，最多 30 道
    const raw = Number(q.size ?? q.count);
    const size = Number.isFinite(raw) && raw > 0 ? Math.min(Math.floor(raw), 30) : 6;
    const items = randomRecipes(db, size, {
      cuisine: q.cuisine,
      category: q.category,
      diet: q.diet
    });
    return { items, total: items.length };
  });

  app.get('/recipes/batch', async (req, reply) => {
    const q = req.query as { ids?: string };
    const ids = (q.ids ?? '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
      .slice(0, 100);
    if (!ids.length) return reply.code(400).send({ error: 'bad_request', message: 'ids 不能为空' });
    const items = getSummariesByIds(db, ids);
    return { items, total: items.length };
  });

  app.get('/recipes/:id', async (req, reply) => {
    const { id } = req.params as { id: string };
    const data = getRecipeById(db, id);
    if (!data) return reply.code(404).send({ error: 'not_found', message: `菜谱 ${id} 不存在` });
    return data;
  });

  app.get('/recipes/:id/related', async (req) => {
    const { id } = req.params as { id: string };
    const data = getRecipeById(db, id);
    if (!data) return { items: [], total: 0 };
    const wanted: string[] = Array.isArray(data.related_ids) ? data.related_ids : [];
    let items = getSummariesByIds(db, wanted);
    if (items.length < 4) {
      const extra = randomRecipes(db, 4 - items.length, { cuisine: data.cuisine?.style });
      const seen = new Set(items.map((i) => i.id));
      items = items.concat(extra.filter((e) => e.id !== id && !seen.has(e.id)));
    }
    return { items: items.filter((i) => i.id !== id), total: items.filter((i) => i.id !== id).length };
  });

  app.get('/search', async (req) => {
    const q = req.query as Record<string, string>;
    const keyword = (q.q ?? '').trim();
    const result = listRecipes(db, {
      page: Number(q.page) || 1,
      pageSize: Number(q.pageSize) || undefined,
      q: keyword || undefined,
      region: q.region as never,
      cuisine: q.cuisine,
      category: q.category as never,
      difficulty: q.difficulty ? (Number(q.difficulty) as never) : undefined,
      flavor: q.flavor,
      diet: q.diet,
      allergen: q.allergen,
      ingredient: q.ingredient,
      maxTime: q.maxTime ? Number(q.maxTime) : undefined,
      sort: (q.sort as never) ?? undefined
    });
    return { ...result, q: keyword };
  });
}
