/**
 * 数据库连接（Drizzle ORM + better-sqlite3）
 * 迁移到 PostgreSQL 时替换 driver，schema 与查询构建器保持不变。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import * as schema from './schema.js';

const here = path.dirname(fileURLToPath(import.meta.url));
/** 仓库根目录：packages/db/src → ../../.. */
export const REPO_ROOT = path.resolve(here, '..', '..', '..');

export function resolveDbPath(explicit?: string): string {
  const p = explicit || process.env.CAIPU_DB_PATH || path.join(REPO_ROOT, 'data', 'db', 'caipu.sqlite');
  fs.mkdirSync(path.dirname(p), { recursive: true });
  return p;
}

export type Db = ReturnType<typeof createDb>;

export function createDb(dbPath?: string) {
  const file = resolveDbPath(dbPath);
  const sqlite = new Database(file);
  sqlite.pragma('journal_mode = WAL');
  sqlite.pragma('foreign_keys = ON');
  const db = drizzle(sqlite, { schema });
  return { db, sqlite, file, schema };
}

export { schema };
// 表定义直接从包根导出，方便 API 层 `import { recipes } from '@caipu/db'`
export * from './schema.js';
