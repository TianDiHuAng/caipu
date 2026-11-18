import type { Metadata } from 'next';
import { api } from '@/lib/api';
import { RecipeGrid, Pagination, categoryZh } from '@/components/RecipeCard';


type Props = { params: { slug: string }; searchParams: { page?: string; difficulty?: string; maxTime?: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const label = categoryZh[params.slug] ?? params.slug;
  return {
    title: `${label}菜谱`,
    description: `${label}类菜谱合集，含分步做法、火候与时间、感官判断线索。`,
    alternates: { canonical: `/categories/${params.slug}` }
  };
}

export const dynamic = 'force-dynamic';

export default async function CategoryDetail({ params, searchParams }: Props) {
  const page = Math.max(1, Number(searchParams?.page) || 1);
  const list = await api.recipes({
    category: params.slug,
    page,
    pageSize: 24,
    difficulty: searchParams?.difficulty,
    maxTime: searchParams?.maxTime
  });
  const label = categoryZh[params.slug] ?? params.slug;
  const items = list?.items ?? [];
  const total = list?.total ?? items.length;

  return (
    <>
      <nav aria-label="面包屑" className="text-sm text-slate-500">
        <a href="/categories">品类</a> / <span>{label}</span>
      </nav>
      <h1 className="mt-2 text-2xl font-bold">{label}</h1>
      <p className="mt-2 text-slate-600">共 {total} 道。</p>
      <form className="mt-3 flex flex-wrap items-end gap-3 text-sm" action={`/categories/${params.slug}`}>
        <label className="flex flex-col gap-1">
          难度
          <select name="difficulty" defaultValue={searchParams?.difficulty ?? ''} className="rounded border border-slate-300 px-2 py-1">
            <option value="">不限</option>
            {[1, 2, 3, 4, 5].map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1">
          最长用时（分钟）
          <input name="maxTime" defaultValue={searchParams?.maxTime ?? ''} inputMode="numeric" className="w-28 rounded border border-slate-300 px-2 py-1" />
        </label>
        <button type="submit" className="rounded bg-brand-600 px-3 py-1.5 text-white hover:bg-brand-700">筛选</button>
      </form>
      <div className="mt-4">
        <RecipeGrid items={items} />
      </div>
      <Pagination total={total} page={page} pageSize={24} basePath={`/categories/${params.slug}`} />
    </>
  );
}
