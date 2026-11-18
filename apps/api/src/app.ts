import Fastify, { type FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import type { Db } from '@caipu/db';
import { getDb } from './db.js';
import { recipeRoutes } from './routes/recipes.js';
import { metaRoutes } from './routes/meta.js';
import { ingredientRoutes } from './routes/ingredients.js';

export interface BuildOptions {
  db?: Db;
  logger?: boolean;
}

/** 构建 Fastify 实例（不监听端口），便于测试用 inject 直接调用 */
export async function buildApp(options: BuildOptions = {}): Promise<FastifyInstance> {
  const db = options.db ?? getDb();
  const app = Fastify({
    logger: options.logger ?? false,
    trustProxy: true,
    ajv: { customOptions: { removeAdditional: false } }
  });

  await app.register(cors, { origin: true, methods: ['GET', 'OPTIONS'] });

  app.get('/health', async () => {
    const one = (s: string) => (db.sqlite.prepare(s).get() as { c: number }).c;
    const counts = {
      recipes: one('SELECT COUNT(*) c FROM recipes'),
      cuisines: one('SELECT COUNT(*) c FROM cuisines'),
      categories: one('SELECT COUNT(*) c FROM categories'),
      ingredients: one('SELECT COUNT(*) c FROM ingredients_dict')
    };
    return {
      ok: true,
      status: 'ok',
      version: 'v1',
      time: new Date().toISOString(),
      counts
    };
  });

  await app.register(recipeRoutes, { prefix: '/api/v1', db });
  await app.register(metaRoutes, { prefix: '/api/v1', db });
  await app.register(ingredientRoutes, { prefix: '/api/v1', db });

  // 性能：只读接口统一给出边缘/CDN 可用的缓存策略；/health 与错误响应不缓存。
  // 数据由导入脚本离线更新，短 TTL + stale-while-revalidate 足以兼顾新鲜度与命中率。
  app.addHook('onSend', async (req, reply, payload) => {
    if (req.method !== 'GET') return payload;
    if (reply.statusCode >= 400) {
      reply.header('Cache-Control', 'no-store');
      return payload;
    }
    if (req.url.startsWith('/api/v1')) {
      reply.header('Cache-Control', 'public, max-age=60, stale-while-revalidate=300');
      reply.header('Vary', 'Accept-Encoding');
      if (typeof payload === 'string' || Buffer.isBuffer(payload)) {
        reply.header('ETag', `W/"${Buffer.byteLength(payload as string).toString(16)}-${String(payload).length.toString(16)}"`);
      }
    } else {
      reply.header('Cache-Control', 'no-store');
    }
    return payload;
  });

  app.setNotFoundHandler(async (req, reply) =>
    reply.code(404).send({ error: 'not_found', message: `路由 ${req.method} ${req.url} 不存在` })
  );

  app.setErrorHandler(async (err, req, reply) => {
    req.log.error?.(err);
    return reply.code(err.statusCode && err.statusCode >= 400 ? err.statusCode : 500).send({
      error: 'internal_error',
      message: err.message
    });
  });

  return app;
}
