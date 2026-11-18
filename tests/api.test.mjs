import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

let app;

function run(cmd, args) {
  const res = spawnSync(cmd, args, { cwd: ROOT, encoding: 'utf8', shell: true });
  if (res.status !== 0) {
    throw new Error(`命令失败: ${cmd} ${args.join(' ')}\n${res.stdout}\n${res.stderr}`);
  }
  return res.stdout;
}

before(async () => {
  run('npx', ['tsx', 'packages/db/src/init.ts', '--reset']);
  run('npx', ['tsx', 'scripts/import.ts', '--reset']);
  const { buildApp } = await import('../apps/api/src/app.ts');
  app = await buildApp({ logger: false });
  await app.ready();
});

after(async () => {
  if (app) await app.close();
});

const api = (url) => app.inject({ method: 'GET', url });

test('GET /health 返回服务状态与数据计数', async () => {
  const res = await api('/health');
  assert.equal(res.statusCode, 200);
  const body = res.json();
  assert.equal(body.status, 'ok');
  assert.ok(body.counts.recipes >= 3, '菜谱数应不少于 3');
  assert.ok(body.counts.cuisines >= 50, '菜系数应不少于 50');
});

test('GET /api/v1/recipes 返回分页结构', async () => {
  const res = await api('/api/v1/recipes');
  assert.equal(res.statusCode, 200);
  const body = res.json();
  assert.equal(typeof body.total, 'number');
  assert.ok(Array.isArray(body.items));
  assert.equal(body.page, 1);
  assert.ok(body.pageSize > 0);
  assert.ok(body.items.length > 0, '默认应返回已发布菜谱');
  const first = body.items[0];
  assert.ok(first.id && first.name?.zh && first.name?.en, '摘要需含中英文名');
});

test('GET /api/v1/recipes/:id 返回完整菜谱', async () => {
  const res = await api('/api/v1/recipes/gongbao-jiding');
  assert.equal(res.statusCode, 200);
  const body = res.json();
  assert.equal(body.id, 'gongbao-jiding');
  assert.equal(body.name.zh, '宫保鸡丁');
  assert.ok(Array.isArray(body.ingredients) && body.ingredients.length >= 2);
  assert.ok(body.steps.length >= 4);
  assert.ok(body.nutrition_estimate.is_estimate === true);
});

test('GET /api/v1/recipes/:id 不存在时返回 404', async () => {
  const res = await api('/api/v1/recipes/not-exist-recipe');
  assert.equal(res.statusCode, 404);
  const body = res.json();
  assert.equal(body.error, 'not_found');
  assert.ok(body.message.includes('不存在'));
});

test('GET /api/v1/recipes 支持按菜系与品类筛选', async () => {
  const byCuisine = (await api('/api/v1/recipes?cuisine=sichuan')).json();
  assert.ok(byCuisine.total >= 3);
  assert.ok(byCuisine.items.every((x) => x.cuisine.style === 'sichuan'));

  const byCategory = (await api('/api/v1/recipes?category=main-tofu')).json();
  assert.ok(byCategory.total >= 1);
  assert.ok(byCategory.items.every((x) => x.category.includes('main-tofu')));
});

test('GET /api/v1/recipes 支持按食材反查与过敏原排除', async () => {
  const byIngredient = (await api('/api/v1/recipes?ingredient=' + encodeURIComponent('花生米'))).json();
  assert.ok(byIngredient.total >= 1);
  assert.ok(byIngredient.items.some((x) => x.id === 'gongbao-jiding'));

  const noPeanut = (await api('/api/v1/recipes?allergen=peanut')).json();
  assert.ok(noPeanut.items.every((x) => !(x.allergens || []).includes('peanut')));
});

test('GET /api/v1/recipes 支持排序与分页参数', async () => {
  const quick = (await api('/api/v1/recipes?sort=quickest&pageSize=2')).json();
  assert.equal(quick.pageSize, 2);
  assert.ok(quick.items.length <= 2);
  if (quick.items.length === 2) {
    assert.ok(quick.items[0].total_min <= quick.items[1].total_min, '按耗时升序排列');
  }
});

test('GET /api/v1/search 返回 q 字段与命中结果', async () => {
  const res = await api('/api/v1/search?q=' + encodeURIComponent('豆腐'));
  assert.equal(res.statusCode, 200);
  const body = res.json();
  assert.equal(body.q, '豆腐');
  assert.ok(body.total >= 1);
  assert.ok(body.items.some((x) => x.id === 'mapo-doufu'));
});

test('GET /api/v1/recipes/random 返回指定数量', async () => {
  const body = (await api('/api/v1/recipes/random?size=2')).json();
  assert.ok(Array.isArray(body.items));
  assert.equal(body.items.length, 2);
  assert.equal(new Set(body.items.map((x) => x.id)).size, 2, '随机结果不应重复');
});

test('GET /api/v1/recipes/batch 按 ids 顺序返回', async () => {
  const body = (await api('/api/v1/recipes/batch?ids=mapo-doufu,gongbao-jiding')).json();
  assert.equal(body.items.length, 2);
  assert.equal(body.items[0].id, 'mapo-doufu');
  assert.equal(body.items[1].id, 'gongbao-jiding');
});

test('GET /api/v1/recipes/:id/related 返回不少于 2 道关联菜谱', async () => {
  const body = (await api('/api/v1/recipes/gongbao-jiding/related')).json();
  assert.ok(Array.isArray(body.items));
  assert.ok(body.items.length >= 2);
  assert.ok(body.items.every((x) => x.id !== 'gongbao-jiding'));
});

test('GET /api/v1/filters 返回完整筛选项', async () => {
  const body = (await api('/api/v1/filters')).json();
  assert.ok(body.regions.length >= 2);
  assert.ok(body.cuisines.length >= 50);
  assert.ok(body.categories.length >= 20);
  assert.ok(body.flavors.length >= 5);
  assert.ok(body.dietTags.length >= 5);
  assert.ok(body.allergens.length >= 10);
  assert.ok(body.difficulties.length === 5, '难度应为 1-5 五档');
  assert.ok(body.cuisines.some((c) => c.value === 'sichuan' && c.count >= 3));
});

test('GET /api/v1/cuisines/:slug 返回菜系信息与品类计数', async () => {
  const body = (await api('/api/v1/cuisines/sichuan')).json();
  assert.equal(body.slug, 'sichuan');
  assert.ok(body.zh && body.en);
  assert.ok(body.count >= 3);
  assert.ok(typeof body.intro === 'string' && body.intro.length > 10);
  assert.ok(Array.isArray(body.categories));
});

test('GET /api/v1/ingredients 支持关键词搜索', async () => {
  const body = (await api('/api/v1/ingredients?q=' + encodeURIComponent('豆腐'))).json();
  assert.ok(body.total >= 1);
  assert.ok(body.items.some((x) => x.key === 'silken-tofu' || x.key === 'firm-tofu'));
});

test('GET /api/v1/ingredients/:key/recipes 返回该食材的菜谱', async () => {
  const body = (await api('/api/v1/ingredients/chicken-thigh/recipes')).json();
  assert.ok(body.total >= 1);
  assert.ok(body.items.some((x) => x.id === 'gongbao-jiding'));
});

test('未知路由返回 404 且带错误码', async () => {
  const res = await api('/api/v1/nope');
  assert.equal(res.statusCode, 404);
  assert.ok(res.json().error);
});
