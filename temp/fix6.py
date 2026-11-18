from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\tests\api.test.mjs")
s = p.read_text(encoding="utf-8")

s = s.replace(
    """  const res = await api('/api/v1/recipes/not-exist-recipe');
  assert.equal(res.statusCode, 404);
  assert.equal(res.json().error.code, 'NOT_FOUND');""",
    """  const res = await api('/api/v1/recipes/not-exist-recipe');
  assert.equal(res.statusCode, 404);
  const body = res.json();
  assert.equal(body.error, 'not_found');
  assert.ok(body.message.includes('不存在'));""",
)

s = s.replace(
    """  if (quick.items.length === 2) {
    assert.ok(quick.items[0].time.total_min <= quick.items[1].time.total_min);
  }""",
    """  if (quick.items.length === 2) {
    assert.ok(quick.items[0].total_min <= quick.items[1].total_min, '按耗时升序排列');
  }""",
)

s = s.replace(
    """  const body = (await api('/api/v1/recipes/random?size=2')).json();
  assert.ok(Array.isArray(body.items));
  assert.equal(body.items.length, Math.min(2, body.total ?? 2));""",
    """  const body = (await api('/api/v1/recipes/random?size=2')).json();
  assert.ok(Array.isArray(body.items));
  assert.equal(body.items.length, 2);
  assert.equal(new Set(body.items.map((x) => x.id)).size, 2, '随机结果不应重复');""",
)

s = s.replace(
    """  const body = (await api('/api/v1/filters')).json();
  assert.ok(body.regions.length >= 2);
  assert.ok(body.cuisines.length >= 50);
  assert.ok(body.categories.length >= 20);
  assert.ok(body.flavors.length >= 5);
  assert.ok(body.dietTags.length >= 5);
  assert.ok(body.allergens.length >= 10);""",
    """  const body = (await api('/api/v1/filters')).json();
  assert.ok(body.regions.length >= 2);
  assert.ok(body.cuisines.length >= 50);
  assert.ok(body.categories.length >= 20);
  assert.ok(body.flavors.length >= 5);
  assert.ok(body.dietTags.length >= 5);
  assert.ok(body.allergens.length >= 10);
  assert.ok(body.difficulties.length === 5, '难度应为 1-5 五档');
  assert.ok(body.cuisines.some((c) => c.value === 'sichuan' && c.count >= 3));""",
)

s = s.replace(
    """  assert.equal(body.slug, 'sichuan');
  assert.ok(body.zh);
  assert.ok(body.recipeCount >= 3);""",
    """  assert.equal(body.slug, 'sichuan');
  assert.ok(body.zh && body.en);
  assert.ok(body.count >= 3);
  assert.ok(typeof body.intro === 'string' && body.intro.length > 10);""",
)

p.write_text(s, encoding="utf-8")

# progress 测试改为按 regions 汇总
q = Path(r"D:\AI\project\marvis_project\caipu\tests\data.test.mjs")
t = q.read_text(encoding="utf-8")
t = t.replace(
    """test('progress.json 结构完整且覆盖全部菜系×品类格子', () => {
  const progress = readJson(path.join(ROOT, 'tasks', 'progress.json'));
  const cells = progress.cells || [];
  assert.ok(cells.length > 100, `格子数 ${cells.length} 偏少`);
  for (const c of cells) {
    assert.ok(c.cuisine && c.category, '格子需含 cuisine 与 category');
    assert.equal(typeof c.target, 'number');
    assert.equal(typeof c.done, 'number');
  }
  const totalTarget = cells.reduce((a, c) => a + c.target, 0);
  assert.ok(totalTarget >= 3000, `总目标 ${totalTarget} 应不少于 3000`);
});""",
    """test('progress.json 结构完整且覆盖全部菜系×品类格子', () => {
  const progress = readJson(path.join(ROOT, 'tasks', 'progress.json'));
  const regions = progress.regions || {};
  const cells = [];
  for (const list of Object.values(regions)) {
    for (const c of list) {
      assert.ok(c.slug && Array.isArray(c.cells), '菜系节点需含 slug 与 cells');
      for (const cell of c.cells) {
        cells.push({ cuisine: c.slug, ...cell });
      }
    }
  }
  assert.equal(cells.length, 423, `格子数应为 423，实际 ${cells.length}`);
  for (const c of cells) {
    assert.ok(c.category, '格子需含 category');
    assert.equal(typeof c.target, 'number');
    assert.equal(typeof c.actual, 'number');
    assert.ok(Array.isArray(c.ids));
  }
  const totalTarget = cells.reduce((a, c) => a + c.target, 0);
  assert.ok(totalTarget >= 3000, `总目标 ${totalTarget} 应不少于 3000`);
  assert.equal(progress.totals.target, totalTarget);
});""",
)
q.write_text(t, encoding="utf-8")
print("ok")
