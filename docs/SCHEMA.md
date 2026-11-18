# SCHEMA — 菜谱数据结构（唯一真相）

> 机器可读版本：`schema/recipe.schema.json`（JSON Schema draft-07）。
> 本文件与 JSON Schema 必须保持同步；任何字段变更需同时修改两处并递增 `schema_version`。

---

## 1. 文件组织

```
data/recipes/{region}/{cuisine}/{id}.json
```

- `region`：`cn`（中国）/ `intl`（外国）
- `cuisine`：菜系 slug，见 `docs/TAXONOMY.md`
- `id`：全库唯一英文 slug，小写，`[a-z0-9-]+`，例如 `gong-bao-ji-ding`

### 兼容性字段

```json
"schema_version": "1.0",
"content_version": 3
```

`schema_version` 用于数据迁移，`content_version` 在每次内容实质修改时 +1。

---

## 2. 完整字段说明

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | ✓ | 全库唯一英文 slug，`^[a-z0-9]+(-[a-z0-9]+)*$` |
| `name` | object | ✓ | `{zh, en, original?}`，`original` 为原文名（如日文汉字、意大利文原拼） |
| `cuisine` | object | ✓ | `{region: "cn"|"intl", style: string}`，`style` 须存在于 TAXONOMY 菜系列表 |
| `category` | string[] | ✓ | 至少 1 项，须存在于 TAXONOMY 品类枚举 |
| `difficulty` | int 1-5 | ✓ | 1=几乎零失败，5=需要专业技巧（如拉面、酥皮、发酵控制） |
| `time` | object | ✓ | `{prep_min, cook_min, total_min}`，`total_min = prep + cook`（允许 ±10% 用于静置/腌制不清零时的取整，校验脚本按等式强校验） |
| `servings` | int 1-12 | ✓ | 基准份量（人份） |
| `flavor` | string[] | ✓ | 口味标签，见 TAXONOMY `flavor` 枚举 |
| `ingredients` | array | ✓ | 分组数组，见 §2.1 |
| `equipment` | string[] | ✓ | 必需器具，至少 1 项 |
| `steps` | array | ✓ | 见 §2.2，至少 4 步（`category` 含 `drink` 且 `difficulty`=1 时至少 3 步） |
| `tips` | string[] | ✓ | 至少 2 条实操建议 |
| `common_mistakes` | string[] | ✓ | 至少 1 条常见失败原因与规避方法 |
| `substitutions` | array | ✓ | `{original, substitute, ratio, note}` |
| `variations` | string[] | ✓ | 至少 1 条：地方变体或家庭简化版 |
| `serving_suggestion` | string | ✓ | 怎么吃、配什么 |
| `storage` | string | ✓ | 保存方式与期限 |
| `nutrition_estimate` | object | ✓ | 见 §2.3，**必须标注估算** |
| `allergens` | string[] | ✓ | 枚举见 TAXONOMY `allergen`；由食材词典推导，不得手填不含的项 |
| `diet_tags` | string[] | ✓ | 枚举见 TAXONOMY `diet_tag`，可为空数组 |
| `food_safety_notes` | string[] | ✓ | 至少 1 条；高风险食材必须写处理要点 |
| `origin_note` | string | ✓ | 来历/文化背景，不确定用「相传」，禁止编造具体年代与人物 |
| `tags` | string[] | ✓ | 自由标签（场景、技法、季节等），≤10 个 |
| `related_ids` | string[] | ✓ | 必须指向真实存在的 id，不得自引用，≤6 个 |
| `status` | enum | ✓ | `draft` / `reviewed` / `published` |
| `image_url` | string \| null | ✓ | 本期为 `null`（不采集图片） |
| `image_credit` | string \| null | ✓ | 本期为 `null` |
| `created_at` | string | ✓ | ISO 8601 日期 `YYYY-MM-DD` |
| `updated_at` | string | ✓ | 同上 |
| `schema_version` | string | ✓ | 当前 `"1.0"` |
| `content_version` | int | ✓ | ≥1 |

### 2.1 `ingredients`

分组对象数组，`group` 只允许 `main`（主料）/ `aux`（辅料）/ `seasoning`（调料）。

```json
{
  "group": "main",
  "items": [
    {
      "name": "鸡腿肉",
      "name_en": "chicken thigh",
      "amount": 300,
      "unit": "g",
      "note": "去骨，切 2cm 丁",
      "substitute": "鸡胸肉（口感偏柴，腌时多加 5ml 油）",
      "optional": false
    }
  ]
}
```

- `amount`：number 或 `null`（仅当 `unit` 为 `"to-taste"` 时允许 null）
- `unit`：枚举 `g` / `ml` / `piece` / `clove` / `slice` / `stalk` / `to-taste` / `pinch`
- `note`：处理方式，必填非空字符串
- `optional`：bool，必填

**「适量」规则**：`unit="to-taste"` 仅允许用于盐、油、胡椒、辣椒、糖、酱油类；且该食材的 `note` 必须给出参考范围（如「约 2g，按口味增减」）。

### 2.2 `steps`

```json
{
  "n": 3,
  "text": "锅烧至冒烟，下 30ml 菜籽油，油面微微起纹时下鸡丁，中大火摊平不要翻动，煎 40 秒至底面金黄再翻。",
  "time_min": 2,
  "heat": "中大火",
  "tip": "鸡丁下锅前把腌汁沥干，否则会溅油且不易上色。",
  "visual_cue": "底面呈浅金黄色，边缘微微焦香，能闻到明显的鸡油香。"
}
```

- `n`：从 1 连续递增
- `time_min`：int ≥0（0 表示瞬间动作，如"关火"）
- `heat`：`大火`/`中大火`/`中火`/`中小火`/`小火`/`微火`/`无火`/`-`（非加热步骤用 `-`）
- `visual_cue`：**必填非空**，判断熟度的外观/气味/声音/触感线索

**食材引用约束**：步骤文本中出现的食材名必须存在于配料表（校验脚本按词典别名匹配）。

### 2.3 `nutrition_estimate`

```json
{
  "basis": "每份（按 2 人份计）",
  "calories_kcal": 420,
  "protein_g": 28,
  "fat_g": 26,
  "carbs_g": 16,
  "sodium_mg": 780,
  "is_estimate": true,
  "disclaimer": "基于食材标准成分表估算，实际值随品牌与用量波动，仅供参考。"
}
```

`is_estimate` 必须为 `true`，`disclaimer` 非空。

---

## 3. 与食材词典的关系

`data/ingredients.json` 是食材名的唯一权威：

```json
{
  "key": "peanut",
  "zh": "花生",
  "en": "peanut",
  "aliases": ["花生米", "去皮花生", "花生碎"],
  "allergens": ["peanut"],
  "category": "nut"
}
```

校验规则：
1. 配料表 `name` 必须能在词典中按 `zh` 或 `aliases` 命中；
2. 菜谱 `allergens` = 所有命中食材 `allergens` 的并集（顺序按枚举固定），**多一个或少一个都报错**。

---

## 4. 版本与迁移

- 字段新增必须向后兼容（新增字段设默认值）。
- 破坏性变更（改名、改类型）需提供 `scripts/migrate-{from}-to-{to}.mjs`。
- 数据库层由 ORM 迁移管理，JSON 层由上述脚本管理，两条线互不干扰。
