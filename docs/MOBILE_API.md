# 移动端对接指南（App / 小程序）

本项目的 API 以「无状态 + 稳定字段 + 规范分页」为目标设计，Web 前端只是其中一个消费者。
App（iOS/Android/Flutter/React Native）与微信小程序可以复用同一套 `/api/v1` 接口，不需要额外后端改造。

## 1. 接入前约定

| 项目 | 约定 |
| --- | --- |
| 基础地址 | 生产环境走 HTTPS，例如 `https://api.example.com/api/v1`；开发期 `http://<PC-IP>:4000/api/v1` |
| 鉴权 | 当前全部为公开只读接口，无 token；若后续加入收藏/用户体系，建议 `Authorization: Bearer <jwt>`，不改变现有接口路径 |
| 请求方法 | 仅 `GET`；`OPTIONS` 用于 CORS 预检 |
| 编码 | 响应 `application/json; charset=utf-8` |
| 缓存 | 响应头已带 `Cache-Control: public, max-age=60, stale-while-revalidate=300` 与弱 `ETag`，可直接接 CDN；客户端建议本地再缓存 `/meta`、`/filters` 1 小时 |
| 超时与重试 | 建议连接超时 5s、读取超时 10s；GET 幂等，可安全重试 1 次 |
| 字段稳定性 | 现有字段只增不改；新增字段对旧客户端必须可忽略 |

## 2. 语言处理（zh / en）

- 所有`name`类字段为对象：`name: { zh, en, original? }`；`steps`/`tips` 等正文为字符串（当前以中文为主，`en` 版本按批次补充到 `name_en`/`step_en` 字段时再开放）。
- 客户端按系统语言选择 `name.zh` 或 `name.en`，缺失时回退 `zh → en → original`。
- 小程序/App 的界面文案不要依赖服务端返回的 label 顺序；`/filters` 返回的 `label` 为中文，英文界面请自行映射或读取 `zh`/`en` 双字段。

## 3. 分页规范

所有列表返回：

```json
{ "items": [], "page": 1, "pageSize": 20, "total": 3, "totalPages": 1, "hasNext": false }
```

- `page` 从 1 开始；`pageSize` 默认 20、上限 60。
- 移动端推荐 `pageSize=10`（列表卡片较大），横向滑动推荐 12。
- 翻页停止条件用 `hasNext === false`，不要用 `items.length < pageSize`。
- 下拉刷新 = `page=1` 重新请求；上拉加载 = `page + 1` 追加，注意按 `id` 去重（随机接口不保证顺序稳定）。

## 4. 关键接口使用场景

### 4.1 启动（首屏）

```http
GET /api/v1/meta        # 分类树、风味、饮食标签、过敏原、难度
GET /api/v1/filters     # 带数量的筛选项，适合筛选面板
GET /api/v1/recipes/random?size=6
```

三个请求可并发；`/meta` 与 `/filters` 落本地缓存（建议 1 小时），首页只拉 `/recipes/random` 与推荐列表。

### 4.2 首页/分类页

```http
GET /api/v1/recipes?page=1&pageSize=10&sort=newest
GET /api/v1/categories
GET /api/v1/categories/:slug/recipes?page=1   # 若网关未开放，等价用法：/recipes?category=<slug>
GET /api/v1/cuisines?region=cn
GET /api/v1/cuisines/:slug
```

`total` 可用于在分类入口展示「共 N 道」。

### 4.3 搜索页

```http
GET /api/v1/search?q=宫保&page=1&pageSize=10
GET /api/v1/search?q=鸡肉&diet=gluten-free&maxTime=30&sort=quickest
```

- `q` 支持中文名、英文名、拼音全拼/首字母（`gongbao`、`gbjd` 均可命中）、食材别名与口语同义词（如「土豆 → 马铃薯」）。
- 带 `q` 时默认 `sort=relevance`，排序权重：菜名 > 拼音/slug > 正文；同档按总时长升序。
- 客户端高亮：接口不返回高亮片段，`<mark>` 高亮由前端对 `name` 文本做本地匹配实现。

### 4.4 详情页

```http
GET /api/v1/recipes/:id
GET /api/v1/recipes/:id/related
```

- 先渲染骨架（名称、时长、难度、份量），再渲染配料与步骤。
- `ingredients` 为分组数组：`[{ group: "main" | "secondary" | "seasoning", items: [...] }]`，分组顺序固定，直接按顺序渲染。
- 步骤对象含 `n/text/time_min/heat/tip/visual_cue`，`visual_cue` 是判断熟度的外观/气味线索，建议在 App 中以小字置灰展示，小程序可用折叠。
- `nutrition_estimate` 为估算值，UI 必须显示「估算」字样。

### 4.5 收藏夹

收藏只存在本地（或自有后端），取数据时批量请求：

```http
GET /api/v1/recipes/batch?ids=a,b,c
```

- 最多 100 个 id；返回顺序与传入一致，不存在的 id 直接跳过，客户端按返回 `id` 回填占位即可。

### 4.6 食材反查（「冰箱里有什么」）

```http
GET /api/v1/ingredients?q=土豆
GET /api/v1/ingredients/:key/recipes?excludeAllergen=peanut,shellfish
```

- `count` 表示该食材被多少菜谱使用，可用于「热门食材」排序。
- `excludeAllergen` 为排除式，适合做「过敏原过滤」开关。

### 4.7 份量换算与单位切换（客户端计算）

服务端返回的是「原始份量」的配料表：`ingredients[].items[].amount`（数字或 `null`）+ `unit`（公制 g/ml/个/勺等）。
换算不请求接口，客户端按以下公式计算：

```
factor = targetServings / recipe.servings
shown  = round(amount * factor, 保留位数按量级自适应)
```

单位切换同样本地完成：

| 食材类型 | 换算 |
| --- | --- |
| 液体（ml） | 1 tbsp ≈ 15 ml，1 tsp ≈ 5 ml，1 cup ≈ 240 ml |
| 面粉/糖等干料 | 1 cup ≈ 120–200 g（按食材密度，词典 `data/ingredients.json` 有 `density_g_per_ml` 时以其为准） |
| 重量 | 1000 g = 1 kg，界面显示时按 >=1000 g 自动切 kg |
| `amount = null` 且 `to_taste = true` | 显示「适量」，并按 `note` 中的参考范围展示（如「约 2–3 g」） |

小程序注意：`WXML` 中不要做浮点累加，建议统一用整数克/毫升存储，最后一步再格式化。

### 4.8 打印/分享

Web 端有 `/recipes/:id/print`。App/小程序不调用打印页，直接用详情数据生成分享卡片；
分享文案建议格式：`「菜名」难度X · 共Y分钟 · Z人份`。

## 5. 小程序特别说明

- 域名白名单：把 API 域名加入「request 合法域名」，HTTPS 必须有效证书。
- 本地开发可用开发者工具「不校验合法域名」开关。
- 小程序无 `localStorage`，等价用 `wx.setStorageSync` 缓存 `/meta`、`/filters`。
- 分包：详情页与搜索页放主包，分类/食材页可放分包，避免首包超 2MB。
- 图片：`image_url` 当前为占位（`/placeholder/*.svg`），上线前替换 CDN 地址；`image_credit` 保留出处署名，不得删除。

## 6. App 特别说明（iOS / Android / Flutter / RN）

- 请求层统一封装：`baseUrl + /api/v1`，集中处理 4xx/5xx 与重试。
- 列表页使用 `FlatList`/`LazyColumn` 的 `onEndReached`，以 `hasNext` 控制。
- 离线缓存：SQLite/Realm 存摘要 + 最近查看的 50 条详情，弱网优先读缓存。
- 深链：`caipu://recipe/<id>` → 详情页；`caipu://search?q=<kw>` → 搜索页。
- 多语言：`Accept-Language` 目前不影响返回（服务端字段同时含 zh/en），客户端自行选字段。

## 7. 错误处理

| 状态码 | `error` | 处理建议 |
| --- | --- | --- |
| 400 | `bad_request` | 参数非法（如 `ids` 为空、`pageSize` 超限），提示并回到默认列表 |
| 404 | `not_found` | 菜品/食材已下线，展示空态并提供返回入口 |
| 500 | `internal_error` | 展示重试按钮，最多重试 1 次 |

错误响应体：`{ "error": "not_found", "message": "路由 GET /api/v1/x 不存在" }`。

## 8. 联调清单

- [ ] `/health` 200 且 `counts.recipes > 0`
- [ ] `/meta` 返回 59 个菜系、26 个品类
- [ ] 列表翻页到最后一页 `hasNext=false`
- [ ] 搜索中文、拼音、英文关键词均能命中
- [ ] 详情页 31 个字段均能渲染，`nutrition_estimate` 带「估算」标识
- [ ] 份量换算 2 人份 ↔ 4 人份数值正确
- [ ] 收藏批量接口顺序与传入一致
- [ ] 断网时展示缓存数据与离线提示
