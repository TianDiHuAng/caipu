/**
 * 冒烟检查：不经网络，直接以 inject 方式验证 API 关键端点。
 * 用法：node scripts/smoke.mjs （或 npx tsx scripts/smoke.mjs）
 * 退出码 0 表示全部通过。
 */
import { buildApp } from '../apps/api/src/app.ts';

const CHECKS = [
  ['/health', (b) => b.ok === true && b.counts.recipes >= 1, '健康检查与计数'],
  ['/api/v1/meta', (b) => b.counts && Array.isArray(b.categories), '元数据'],
  ['/api/v1/filters', (b) => b.flavors.length === 14 && b.allergens.length === 14 && b.dietTags.length === 9, '筛选项全量'],
  ['/api/v1/cuisines', (b) => b.total === 59, '菜系列表 59'],
  ['/api/v1/cuisines/sichuan', (b) => b.slug === 'sichuan' && b.categories.length >= 1, '菜系详情'],
  ['/api/v1/categories', (b) => b.total === 26, '品类 26'],
  ['/api/v1/recipes?pageSize=5', (b) => b.items.length >= 1 && typeof b.total === 'number', '菜谱分页'],
  ['/api/v1/recipes?cuisine=sichuan', (b) => b.items.every((x) => x.cuisine.style === 'sichuan'), '按菜系筛选'],
  ['/api/v1/recipes/random?size=2', (b) => b.items.length === 2, '随机推荐'],
  ['/api/v1/recipes/batch?ids=gongbao-jiding', (b) => b.items[0]?.id === 'gongbao-jiding', '批量取摘要'],
  ['/api/v1/recipes/gongbao-jiding', (b) => b.id && Array.isArray(b.steps) && b.steps.length >= 4, '菜谱详情'],
  ['/api/v1/recipes/gongbao-jiding/related', (b) => Array.isArray(b.items) && b.items.every((x) => x.id !== 'gongbao-jiding'), '关联菜谱'],
  ['/api/v1/search?q=' + encodeURIComponent('鸡'), (b) => b.q === '鸡', '搜索回显'],
  ['/api/v1/ingredients?q=' + encodeURIComponent('豆瓣'), (b) => b.total >= 1, '食材搜索'],
  ['/api/v1/ingredients/doubanjiang', (b) => b.key === 'doubanjiang', '食材详情'],
  ['/api/v1/ingredients/doubanjiang/recipes', (b) => b.items.length >= 1, '食材反查菜谱'],
  ['/api/v1/recipes/not-exist', (b) => b.error === 'not_found', '404 结构', 404]
];

const app = await buildApp({ logger: false });
await app.ready();

let failed = 0;
for (const [url, check, label, expectStatus = 200] of CHECKS) {
  const res = await app.inject({ method: 'GET', url });
  let body;
  try {
    body = res.json();
  } catch {
    body = null;
  }
  const ok = res.statusCode === expectStatus && body && check(body);
  if (!ok) {
    failed += 1;
    console.log(`[FAIL] ${label} (${url}) status=${res.statusCode} body=${res.body.slice(0, 200)}`);
  } else {
    console.log(`[ OK ] ${label}`);
  }
}

await app.close();
console.log(`\n${CHECKS.length - failed}/${CHECKS.length} 通过`);
process.exit(failed ? 1 : 0);
