/**
 * 界面 i18n（zh / en）。
 * 设计：菜谱数据本身是双语的（name.zh / name.en），界面文案集中在字典里；
 * 语言通过 ?lang=en 设置并写入 cookie，服务端渲染时直接读到，首屏即为目标语言（无闪烁）。
 * 路由级前缀（/en/...）留给 App/小程序统一接入时再做，理由写在 docs/DECISIONS.md。
 */
export type Locale = 'zh' | 'en';

export const LOCALES: Locale[] = ['zh', 'en'];

type Dict = Record<string, { zh: string; en: string }>;

export const DICT = {
  site: { zh: '中外菜谱', en: 'World Recipes' },
  navHome: { zh: '首页', en: 'Home' },
  navCuisines: { zh: '菜系', en: 'Cuisines' },
  navCategories: { zh: '品类', en: 'Categories' },
  navIngredients: { zh: '食材反查', en: 'By ingredient' },
  navSearch: { zh: '搜索', en: 'Search' },
  heroTitle: { zh: '结构化收录中外菜谱', en: 'Structured recipes from China and around the world' },
  heroDesc: {
    zh: '分步做法、火候与时间、判断熟度的感官线索、家庭简化版、替代食材、过敏原与食品安全提示。',
    en: 'Step-by-step method, heat and timing, sensory doneness cues, home simplified versions, substitutions, allergens and food-safety notes.'
  },
  searchPlaceholder: {
    zh: '搜索菜名、食材或菜系，如：红烧肉 / 番茄 / 川菜',
    en: 'Search dish, ingredient or cuisine, e.g. mapo tofu / tomato / Sichuan'
  },
  searchButton: { zh: '搜索', en: 'Search' },
  totalRecipes: { zh: '已收录', en: 'Recipes' },
  recipesUnit: { zh: '道菜谱', en: '' },
  byCuisine: { zh: '按菜系浏览', en: 'Browse by cuisine' },
  byCategory: { zh: '按品类浏览', en: 'Browse by category' },
  byIngredient: { zh: '食材反查', en: 'Browse by ingredient' },
  cuisineNav: { zh: '菜系导航', en: 'Cuisines' },
  cuisineNavDesc: {
    zh: '中国八大菜系与各地风味、世界各地菜系，均按标准化的菜系标识归类。',
    en: 'The eight great Chinese cuisines, regional Chinese styles and world cuisines, all mapped to stable cuisine slugs.'
  },
  categoryNav: { zh: '按品类浏览', en: 'Browse by category' },
  latest: { zh: '最新收录', en: 'Recently added' },
  viewAllLatest: { zh: '查看全部最新菜谱 →', en: 'All latest recipes →' },
  randomTitle: { zh: '今天吃什么', en: 'What to cook today' },
  randomDesc: {
    zh: '每次刷新随机推荐，可用于「不知道做什么」的场景。',
    en: 'Random picks on every refresh, for when you cannot decide.'
  },
  difficulty: { zh: '难度', en: 'Level' },
  minutes: { zh: '分钟', en: 'min' },
  flavor: { zh: '口味', en: 'Flavor' },
  empty: { zh: '暂无菜谱。', en: 'No recipes yet.' },
  prev: { zh: '上一页', en: 'Prev' },
  next: { zh: '下一页', en: 'Next' },
  pageInfo: { zh: '页', en: 'page' },
  footerNote: {
    zh: '菜谱文本均为原创撰写，图片字段留空或标注来源，不转载第三方图片。',
    en: 'All recipe text is original. Image fields are left blank or credited; no third-party images are reused.'
  },
  footerDisclaimer: {
    zh: '营养数据为估算值，仅供参考；食品安全提示请以当地监管机构建议为准。',
    en: 'Nutrition figures are estimates. Food-safety guidance follows local regulators.'
  },
  langSwitch: { zh: 'English', en: '中文' }
} satisfies Dict;

export function t(key: keyof typeof DICT, locale: Locale): string {
  return DICT[key]?.[locale] ?? String(key);
}

export const dictFor = (locale: Locale) => (key: keyof typeof DICT) => t(key, locale);

export function htmlLang(locale: Locale): string {
  return locale === 'en' ? 'en' : 'zh-CN';
}
