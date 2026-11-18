import { createDb, type Db } from '@caipu/db';

let cached: Db | null = null;

/** 进程内单例（无状态 API，仅缓存连接） */
export function getDb(): Db {
  if (!cached) cached = createDb();
  return cached;
}
