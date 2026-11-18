import type { Metadata } from 'next';
import { api } from '@/lib/api';
import { RecipeGrid, Pagination } from '@/components/RecipeCard';


type Props = { params: { slug: string }; searchParams: { page?: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const info: any = await api.ingredient(params.slug);
  const label = info?.zh ?? params.slug;
  return {
    title: `用${label}做的菜`,
    description: `收录所有用到${label}的菜谱，按菜系与品类分类。`,
    alternates: { canonical: `/ingredients/${params.slug}` }
  };
}

export const dynamic = 'force-dynamic';

export default async function IngredientDetail({ params, searchParams }: Props) {
  const page = Math.max(1, Number(searchParams?.page) || 1);
  const [info, list] = await Promise.all([api.ingredient(params.slug), api.ingredientRecipes(params.slug, page)]);
  const label = (info as any)?.zh ?? params.slug;
  const items = list?.items ?? [];
  const total = list?.total ?? items.length;

  return (
    <>
      <nav aria-label="面包屑" className="text-sm text-slate-500">
        <a href="/ingredients">食材反查</a> / <span>{label}</span>
      </nav>
      <h1 className="mt-2 text-2xl font-bold">用{label}做的菜</h1>
      <p className="mt-2 text-slate-600">
        共 {total} 道。{(info as any)?.en ? <span className="ml-1 text-slate-500">{String((info as any).en)}</span> : null}
      </p>
      {(info as any)?.allergens?.length ? (
        <p className="mt-2 text-sm text-amber-800">过敏原提示：{(info as any).allergens.join('、')}</p>
      ) : null}
      <div className="mt-4">
        <RecipeGrid items={items} />
      </div>
      <Pagination total={total} page={page} pageSize={24} basePath={`/ingredients/${params.slug}`} />
    </>
  );
}
