import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { api } from '@/lib/api';
import { RecipeGrid, Pagination } from '@/components/RecipeCard';


type Props = { params: { slug: string }; searchParams: { page?: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const info: any = await api.cuisine(params.slug);
  const label = info?.zh ?? info?.name?.zh ?? params.slug;
  return {
    title: `${label}菜谱`,
    description: `${label}经典菜谱合集：分步做法、火候时间、判断熟度的线索与家庭简化版。`,
    alternates: { canonical: `/cuisines/${params.slug}` }
  };
}

export const dynamic = 'force-dynamic';

export default async function CuisineDetail({ params, searchParams }: Props) {
  const page = Math.max(1, Number(searchParams?.page) || 1);
  const [info, list] = await Promise.all([
    api.cuisine(params.slug),
    api.recipes({ cuisine: params.slug, page, pageSize: 24 })
  ]);
  if (!info && !list) notFound();
  const label = (info as any)?.zh ?? (info as any)?.name?.zh ?? params.slug;
  const items = list?.items ?? (info as any)?.recipes?.items ?? [];
  const total = list?.total ?? (info as any)?.recipes?.total ?? items.length;

  return (
    <>
      <nav aria-label="面包屑" className="text-sm text-slate-500">
        <a href="/cuisines">菜系</a> / <span>{label}</span>
      </nav>
      <h1 className="mt-2 text-2xl font-bold">{label}菜谱</h1>
      <p className="mt-2 text-slate-600">共 {total} 道。可按难度、时长在搜索页进一步筛选。</p>
      <div className="mt-4">
        <RecipeGrid items={items} />
      </div>
      <Pagination total={total} page={page} pageSize={24} basePath={`/cuisines/${params.slug}`} />
    </>
  );
}
