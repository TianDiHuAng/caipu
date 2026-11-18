import type { Metadata } from 'next';
import { api } from '@/lib/api';
import { getLocale } from '@/lib/locale-server';
import { RecipeGrid, Pagination, categoryZh, flavorZh } from '@/components/RecipeCard';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = { title: '搜索菜谱', description: '按菜名、食材、菜系、品类、难度、口味、饮食标签与时长搜索菜谱。' };

const DIETS: Array<[string, string]> = [
  ['vegetarian', '素食'], ['vegan', '纯素'], ['gluten-free', '无麸质'], ['dairy-free', '无乳制品'],
  ['halal', '清真'], ['low-calorie', '低卡'], ['high-protein', '高蛋白']
];

export default async function SearchPage({ searchParams }: { searchParams: Record<string, string | undefined> }) {
  const locale = getLocale();
  const page = Math.max(1, Number(searchParams.page) || 1);
  const params = {
    q: searchParams.q,
    cuisine: searchParams.cuisine,
    category: searchParams.category,
    difficulty: searchParams.difficulty,
    flavor: searchParams.flavor,
    diet: searchParams.diet,
    maxTime: searchParams.maxTime,
    ingredient: searchParams.ingredient,
    sort: searchParams.sort,
    page,
    pageSize: 24
  };
  const [list, cuisines, categories] = await Promise.all([api.recipes(params), api.cuisines(), api.categories()]);
  const items = list?.items ?? [];
  const total = list?.total ?? items.length;

  return (
    <>
      <h1 className="text-2xl font-bold">{locale === 'en' ? 'Search recipes' : '搜索菜谱'}</h1>
      <form method="get" action="/search" className="mt-4 grid gap-3 rounded border border-slate-200 p-4 sm:grid-cols-2 lg:grid-cols-3">
        <label className="flex flex-col gap-1 text-sm">
          关键词（菜名 / 描述）
          <input name="q" defaultValue={searchParams.q ?? ''} className="rounded border border-slate-300 px-2 py-1.5" />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          食材
          <input name="ingredient" defaultValue={searchParams.ingredient ?? ''} placeholder="如：五花肉" className="rounded border border-slate-300 px-2 py-1.5" />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          菜系
          <select name="cuisine" defaultValue={searchParams.cuisine ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">不限</option>
            {((cuisines as any)?.items ?? []).map((c: any) => (
              <option key={c.slug} value={c.slug}>{c.zh ?? c.slug}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          品类
          <select name="category" defaultValue={searchParams.category ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">不限</option>
            {((categories as any)?.items ?? []).map((c: any) => (
              <option key={c.slug} value={c.slug}>{categoryZh[c.slug] ?? c.zh ?? c.slug}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          难度
          <select name="difficulty" defaultValue={searchParams.difficulty ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">不限</option>
            {[1, 2, 3, 4, 5].map((d) => <option key={d} value={d}>{d} 级</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          口味
          <select name="flavor" defaultValue={searchParams.flavor ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">不限</option>
            {Object.entries(flavorZh).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          饮食标签
          <select name="diet" defaultValue={searchParams.diet ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">不限</option>
            {DIETS.map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          最长用时（分钟）
          <input name="maxTime" defaultValue={searchParams.maxTime ?? ''} inputMode="numeric" className="rounded border border-slate-300 px-2 py-1.5" />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          排序
          <select name="sort" defaultValue={searchParams.sort ?? ''} className="rounded border border-slate-300 px-2 py-1.5">
            <option value="">相关度 / 默认</option>
            <option value="latest">最新</option>
            <option value="time-asc">用时从短到长</option>
            <option value="difficulty-asc">难度从低到高</option>
          </select>
        </label>
        <div className="flex items-end gap-2">
          <button type="submit" className="rounded bg-brand-600 px-4 py-1.5 text-white hover:bg-brand-700">搜索</button>
        </div>
      </form>

      <p className="mt-4 text-sm text-slate-600">
        {searchParams.q || searchParams.ingredient ? '搜索结果' : '全部菜谱'}：共 {total} 道
      </p>
      <div className="mt-3">
        <RecipeGrid items={items} q={typeof searchParams.q === 'string' ? searchParams.q : ''} />
      </div>
      <Pagination total={total} page={page} pageSize={24} basePath={`/search?${new URLSearchParams(Object.entries(searchParams).filter(([k, v]) => k !== 'page' && v) as [string, string][]).toString()}`} />
    </>
  );
}
