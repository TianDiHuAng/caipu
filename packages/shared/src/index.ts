/**
 * @caipu/shared —— 全端共用类型与纯函数（网站 / App / 小程序 复用）
 * 与 schema/recipe.schema.json 保持一一对应。
 */

export type Region = 'cn' | 'intl';
export type Tier = 'A' | 'B' | 'C';
export type Unit = 'g' | 'ml' | 'piece' | 'clove' | 'slice' | 'stalk' | 'pinch' | 'to-taste';
export type IngredientGroup = 'main' | 'aux' | 'seasoning';
export type Difficulty = 1 | 2 | 3 | 4 | 5;
export type RecipeStatus = 'draft' | 'reviewed' | 'published';
export type Heat = '大火' | '中大火' | '中火' | '中小火' | '小火' | '微火' | '无火' | '余温' | '热油' | '高温' | '中温' | '低温';

export interface LocalizedName {
  zh: string;
  en: string;
  original?: string;
}

export interface CuisineRef {
  region: Region;
  style: string;
}

export interface TimeInfo {
  prep_min: number;
  cook_min: number;
  total_min: number;
}

export interface IngredientItem {
  name: string;
  name_en?: string;
  amount: number;
  unit: Unit;
  note?: string;
  substitute?: string;
  optional?: boolean;
}

export interface IngredientBlock {
  group: IngredientGroup;
  items: IngredientItem[];
}

export interface Step {
  n: number;
  text: string;
  time_min: number;
  heat: Heat;
  tip: string;
  visual_cue: string;
}

export interface NutritionEstimate {
  calories_kcal?: number;
  protein_g?: number;
  fat_g?: number;
  carbs_g?: number;
  sodium_mg?: number;
  is_estimate: true;
  note?: string;
}

export interface Recipe {
  schema_version: string;
  content_version: number;
  id: string;
  name: LocalizedName;
  cuisine: CuisineRef;
  category: string[];
  difficulty: Difficulty;
  time: TimeInfo;
  servings: number;
  flavor: string[];
  ingredients: IngredientBlock[];
  equipment: string[];
  steps: Step[];
  tips: string[];
  common_mistakes: string[];
  substitutions: string[];
  variations: string[];
  serving_suggestion: string;
  storage: string;
  nutrition_estimate: NutritionEstimate;
  allergens: string[];
  diet_tags: string[];
  food_safety_notes: string;
  origin_note: string;
  tags: string[];
  related_ids: string[];
  status: RecipeStatus;
  image_url: string | null;
  image_credit: string | null;
  created_at: string;
  updated_at: string;
}

/** 列表页使用的轻量摘要 */
export interface RecipeSummary {
  id: string;
  name: LocalizedName;
  cuisine: CuisineRef;
  category: string[];
  difficulty: Difficulty;
  total_min: number;
  servings: number;
  flavor: string[];
  diet_tags: string[];
  allergens: string[];
  image_url: string | null;
  status: RecipeStatus;
}

export interface Paginated<T> {
  items: T[];
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
}

export interface RecipeListQuery {
  page?: number;
  pageSize?: number;
  cuisine?: string;
  region?: Region;
  category?: string;
  difficulty?: Difficulty;
  flavor?: string;
  diet?: string;
  ingredient?: string;
  q?: string;
  maxTime?: number;
  sort?: 'relevance' | 'newest' | 'quickest' | 'easiest' | 'name';
}

/* ------------------------------------------------------------------ */
/* 单位与换算                                                          */
/* ------------------------------------------------------------------ */

export const UNIT_LABELS: Record<Unit, { zh: string; en: string }> = {
  g: { zh: '克', en: 'g' },
  ml: { zh: '毫升', en: 'ml' },
  piece: { zh: '个', en: 'piece' },
  clove: { zh: '瓣', en: 'clove' },
  slice: { zh: '片', en: 'slice' },
  stalk: { zh: '根', en: 'stalk' },
  pinch: { zh: '撮', en: 'pinch' },
  'to-taste': { zh: '适量', en: 'to taste' }
};

/** 常见厨房计量的毫升当量，用于「茶匙/汤匙/杯」辅助显示 */
export const KITCHEN_MEASURES = [
  { key: 'tsp', label: '茶匙', ml: 5 },
  { key: 'tbsp', label: '汤匙', ml: 15 },
  { key: 'cup', label: '杯', ml: 240 }
] as const;

/** 按份量缩放用量，输出对齐到人类可读精度 */
export function scaleAmount(amount: number, baseServings: number, targetServings: number): number {
  if (!baseServings || !targetServings) return amount;
  const raw = (amount * targetServings) / baseServings;
  return roundSmart(raw);
}

/** 小于 10 保留一位小数、10~100 取整数、100 以上取 5 的倍数 */
export function roundSmart(v: number): number {
  if (v <= 0) return 0;
  if (v < 1) return Math.round(v * 100) / 100;
  if (v < 10) return Math.round(v * 10) / 10;
  if (v < 100) return Math.round(v);
  return Math.round(v / 5) * 5;
}

/** 克/毫升数值转厨房计量辅助文案，如 15g → "约 1 汤匙" */
export function toKitchenMeasure(amount: number, unit: Unit): string | null {
  if (unit !== 'g' && unit !== 'ml') return null;
  for (const m of [...KITCHEN_MEASURES].reverse()) {
    if (amount >= m.ml) {
      const n = amount / m.ml;
      if (Math.abs(n - Math.round(n)) < 0.12 && Math.round(n) > 0) return `约 ${Math.round(n)} ${m.label}`;
    }
  }
  if (amount < 5) return null;
  return null;
}

export function formatAmount(amount: number, unit: Unit): string {
  if (unit === 'to-taste') return '适量';
  const v = roundSmart(amount);
  const label = UNIT_LABELS[unit]?.zh ?? unit;
  if (unit === 'g' || unit === 'ml') return `${v}${label}`;
  return `${v}${label}`;
}

/* ------------------------------------------------------------------ */
/* 难度 / 时间展示                                                     */
/* ------------------------------------------------------------------ */

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  1: '很简单',
  2: '简单',
  3: '中等',
  4: '较难',
  5: '大厨级'
};

export function formatDuration(min: number): string {
  if (!min || min <= 0) return '—';
  if (min < 60) return `${min} 分钟`;
  const h = Math.floor(min / 60);
  const m = min % 60;
  return m ? `${h} 小时 ${m} 分钟` : `${h} 小时`;
}

/* ------------------------------------------------------------------ */
/* 筛选参数序列化                                                      */
/* ------------------------------------------------------------------ */

export function buildQueryString(q: RecipeListQuery): string {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(q)) {
    if (v === undefined || v === null || v === '') continue;
    sp.set(k, String(v));
  }
  return sp.toString();
}

export function parsePageParams(
  raw: Record<string, unknown>,
  defaults: { page: number; pageSize: number; maxPageSize: number }
): { page: number; pageSize: number } {
  const toInt = (v: unknown, d: number) => {
    const n = Number.parseInt(String(v ?? ''), 10);
    return Number.isFinite(n) && n > 0 ? n : d;
  };
  const page = toInt(raw.page, defaults.page);
  const pageSize = Math.min(toInt(raw.pageSize, defaults.pageSize), defaults.maxPageSize);
  return { page, pageSize };
}

export function paginate<T>(items: T[], total: number, page: number, pageSize: number): Paginated<T> {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  return {
    items,
    page,
    pageSize,
    total,
    totalPages,
    hasNext: page < totalPages
  };
}
