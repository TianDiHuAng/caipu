export type LocalizedText = { zh: string; en: string; original?: string };

export type Cuisine = { region: string; style: string };

export type RecipeSummary = {
  id: string;
  name: LocalizedText;
  cuisine: Cuisine;
  category: string[];
  difficulty: number;
  total_min?: number;
  prep_min?: number;
  cook_min?: number;
  servings?: number;
  flavor?: string[];
  diet_tags?: string[];
  allergens?: string[];
  image_url?: string | null;
  status?: string;
  time?: { prep_min?: number; cook_min?: number; total_min?: number };
};

export type IngredientRow = {
  name: string;
  name_en?: string;
  amount?: number | string;
  unit?: string;
  note?: string;
  substitute?: string;
  optional?: boolean;
};

export type IngredientGroup = {
  group: 'main' | 'aux' | 'seasoning' | string;
  items: IngredientRow[];
};

export type Substitution = { original: string; substitute: string; ratio?: string; note?: string };

export type StepRow = {
  n: number;
  text: string;
  time_min?: number;
  heat?: string;
  tip?: string;
  visual_cue?: string;
};

export type Recipe = RecipeSummary & {
  ingredients: IngredientGroup[];
  equipment?: string[];
  steps: StepRow[];
  tips?: string[];
  common_mistakes?: string[];
  substitutions?: Substitution[];
  variations?: string[];
  serving_suggestion?: string;
  storage?: string;
  nutrition_estimate?: Record<string, unknown>;
  allergens?: string[];
  food_safety_notes?: string[];
  origin_note?: string;
  tags?: string[];
  related_ids?: string[];
  status?: string;
  created_at?: string;
  updated_at?: string;
};

export type Paged<T> = {
  items: T[];
  total: number;
  page?: number;
  pageSize?: number;
  totalPages?: number;
  hasNext?: boolean;
};

export type CuisineNode = { slug: string; region?: string; zh: string; en?: string; count?: number; intro?: string };
export type CategoryNode = { slug: string; zh: string; en?: string; count?: number };

const SERVER_BASE = process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:4000';
const base = () => (typeof window === 'undefined' ? SERVER_BASE : '');

async function getJson<T>(path: string, revalidate = 60): Promise<T | null> {
  const url = `${base()}/api/v1${path}`;
  try {
    const res = await fetch(url, { next: { revalidate }, headers: { accept: 'application/json' } });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

function qs(params: Record<string, string | number | undefined>): string {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && `${v}` !== '') sp.set(k, String(v));
  }
  const s = sp.toString();
  return s ? `?${s}` : '';
}

export const api = {
  recipes: (params: Record<string, string | number | undefined> = {}, revalidate = 60) =>
    getJson<Paged<RecipeSummary>>(`/recipes${qs(params)}`, revalidate),
  random: (size = 6) => getJson<Paged<RecipeSummary>>(`/recipes/random${qs({ size })}`, 0),
  recipe: (id: string) => getJson<Recipe>(`/recipes/${encodeURIComponent(id)}`),
  related: (id: string) => getJson<Paged<RecipeSummary>>(`/recipes/${encodeURIComponent(id)}/related`),
  search: (params: Record<string, string | number | undefined>) =>
    getJson<Paged<RecipeSummary>>(`/search${qs(params)}`, 0),
  cuisines: () => getJson<{ items: CuisineNode[] }>('/cuisines', 300),
  cuisine: (slug: string) => getJson<CuisineNode>(`/cuisines/${encodeURIComponent(slug)}`, 300),
  categories: () => getJson<{ items: CategoryNode[] }>('/categories', 300),
  ingredients: (q?: string) =>
    getJson<{ items: Array<{ key: string; zh: string; en?: string; allergens?: string[]; recipeCount?: number }> }>(
      `/ingredients${q ? `?q=${encodeURIComponent(q)}` : ''}`,
      300
    ),
  ingredient: (key: string) =>
    getJson<{ key: string; zh: string; en?: string; allergens?: string[]; aliases?: string[]; recipeCount?: number }>(
      `/ingredients/${encodeURIComponent(key)}`,
      300
    ),
  ingredientRecipes: (key: string, page = 1) =>
    getJson<Paged<RecipeSummary>>(`/ingredients/${encodeURIComponent(key)}/recipes${qs({ page })}`, 60),
  filters: () => getJson<Record<string, unknown>>('/filters', 600),
  meta: () => getJson<Record<string, unknown>>('/meta', 600)
};

export const SITE = {
  name: '味典 Recipe Canon',
  tagline: '中外菜谱大全 · 结构化做法与安全提示',
  url: process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000',
  locale: 'zh-CN'
};
