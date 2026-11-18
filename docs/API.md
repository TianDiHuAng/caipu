# API 参考（v1）

基础路径：`/api/v1`。所有接口无状态、只读、支持跨域（开发期 `origin: true`）。
响应统一为 JSON（UTF-8），时间字段为 `YYYY-MM-DD`，无时区概念。

## 约定

### 分页

列表类接口统一返回：

```json
{
  "items": [],
  "page": 1,
  "pageSize": 20,
  "total": 3,
  "totalPages": 1,
  "hasNext": false
}
```

| 参数 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| page | int | 1 | 页码，从 1 开始 |
| pageSize | int | 20 | 每页条数，上限 60 |

### 错误

```json
{ "error": "not_found", "message": "菜谱 xxx 不存在" }
```

| HTTP | error | 场景 |
| --- | --- | --- |
| 400 | bad_request | 参数缺失或非法 |
| 404 | not_found | 资源不存在 / 路由不存在 |
| 500 | internal_error | 未捕获异常 |

### 菜谱摘要 vs 详情

- **摘要**（列表 / 随机 / 批量 / 关联返回）：`id, name{zh,en,original}, cuisine{region,style}, category[], difficulty, total_min, servings, flavor[], diet_tags[], allergens[], image_url, status`
- **详情**（`GET /recipes/:id`）：完整菜谱对象，字段见 `docs/SCHEMA.md`，含 `ingredients / steps / tips / nutrition_estimate` 等全部 31 个必备字段。

### 筛选语义

| 参数 | 语义 |
| --- | --- |
| `region` | 精确匹配 `cn` / `intl` |
| `cuisine` | 菜系 slug，精确匹配 |
| `category` | 品类 slug，菜谱 `category[]` 包含即命中 |
| `difficulty` | 1–5，`minDifficulty` 语义不使用，按精确值匹配 |
| `flavor` | 多个用英文逗号分隔，AND 语义 |
| `diet` | 多个用英文逗号分隔，AND 语义（如 `vegetarian,gluten-free`） |
| `allergen` | 多个用英文逗号分隔，**排除式**（返回不含这些过敏原的菜谱） |
| `ingredient` | 多个用英文逗号分隔，AND 语义（同时含全部食材） |
| `maxTime` | `total_min <= maxTime` |
| `q` | 关键词，命中中英文名、菜系、品类、风味、饮食标签、tags、食材名、来历 |
| `sort` | `newest`(默认) · `quickest` · `easiest` · `name` · `relevance`（带 `q` 时默认） |

未指定 `status` 时只返回 `published`；传 `status=draft|reviewed|published` 可查看其他状态（供后台/预审使用）。

## 元数据

### `GET /health`

```json
{ "ok": true, "version": "1.0.0", "counts": { "recipes": 3, "cuisines": 59, "categories": 26, "ingredients": 271 } }
```

### `GET /meta`

返回 `{ schemaVersion, counts, regions[], categories[], flavors[], dietTags[], allergens[], difficulties[] }`，供客户端启动时缓存字典。

### `GET /cuisines?region=cn`

```json
{ "items": [{ "slug": "sichuan", "zh": "川菜", "en": "Sichuan", "region": "cn", "tier": "A", "intro": "…", "count": 3 }], "total": 59 }
```

### `GET /cuisines/:slug`

菜系详情 + 该菜系下各品类实际数量（按数量降序）：

```json
{ "slug": "sichuan", "zh": "川菜", "count": 3, "categories": [{ "slug": "main-meat", "count": 2 }] }
```

### `GET /categories`

`{ items: [{ slug, zh, en, desc, count }], total }`

### `GET /filters`

一次取回所有筛选项（含中文 label 与当前数量）。风味 / 饮食标签 / 过敏原取 `data/taxonomy.json` 全量，数量为 0 也会返回，保证客户端下拉框稳定。

```json
{
  "regions": [{ "value": "cn", "label": "中国" }],
  "cuisines": [{ "value": "sichuan", "label": "川菜", "region": "cn", "count": 3 }],
  "categories": [{ "value": "main-meat", "label": "荤菜", "count": 2 }],
  "difficulties": [{ "value": 1, "label": "1" }],
  "flavors": [{ "value": "spicy", "label": "香辣", "count": 3 }],
  "dietTags": [{ "value": "vegetarian", "label": "素食", "count": 0 }],
  "allergens": [{ "value": "gluten", "label": "麸质", "count": 3 }],
  "maxTimeOptions": [15, 30, 45, 60, 120]
}
```

## 菜谱

### `GET /recipes`

分页摘要列表，支持全部筛选参数。示例：`/api/v1/recipes?cuisine=sichuan&difficulty=3&sort=quickest&pageSize=10`。

### `GET /recipes/random?size=6`

随机推荐。`size` 与 `count` 等价，上限 30；可选 `cuisine / category / diet` 缩小范围。返回 `{ items, total }`。

### `GET /recipes/batch?ids=a,b,c`

按传入顺序返回摘要，最多 100 个 id，不存在的 id 直接跳过（用于收藏夹、购物清单等场景，避免 N 次请求）。空 `ids` 返回 400。

### `GET /recipes/:id`

完整菜谱详情。不存在返回 404。

### `GET /recipes/:id/related`

相关菜谱摘要。先取 `related_ids`，不足 4 条时用同菜系随机菜补齐；始终排除自身。返回 `{ items, total }`。

### `GET /search?q=宫保`

搜索接口，返回分页结构并回显 `q`。与 `/recipes?q=` 的差别是：`q` 缺失时不做关键词过滤（返回全部），便于前端复用同一组件。

## 食材反查

### `GET /ingredients?q=豆瓣`

食材词典搜索，返回 `{ items: [{ key, zh, en, aliases[], allergens[], count }], total }`，`count` 为该食材被多少菜谱使用。

### `GET /ingredients/:key`

词典条目详情（含别名、过敏原、单位换算提示）。

### `GET /ingredients/:key/recipes?page=1&pageSize=20`

用到该食材的菜谱摘要列表。支持 `excludeAllergen` 参数（逗号分隔）做排除。

## 客户端建议

1. 启动时并发请求 `/meta` 与 `/filters` 并本地缓存（建议 1 小时），减少首屏请求。
2. 列表页用摘要即可，进入详情页再取全量，避免首屏流量过大。
3. 收藏夹批量取数据优先用 `/recipes/batch` 而非循环调用详情。
4. `pageSize` 建议：Web 列表 12–24，移动端列表 10，最大不超过 60。
5. 所有接口可直接被 App / 小程序 / SSR 复用，CORS 已开启；生产环境请在网关层加限流与缓存。
