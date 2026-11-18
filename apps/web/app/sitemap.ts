import type { MetadataRoute } from 'next';
import { api, SITE } from '@/lib/api';

export const dynamic = 'force-dynamic';

async function allRecipeIds(): Promise<string[]> {
  const ids: string[] = [];
  for (let page = 1; page <= 200; page++) {
    const res = await api.recipes({ page, pageSize: 100 });
    if (!res?.items?.length) break;
    ids.push(...res.items.map((r) => r.id));
    if (res.items.length < 100) break;
  }
  return ids;
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = SITE.url;
  const staticRoutes = ['', '/cuisines', '/categories', '/ingredients', '/search'].map((p) => ({
    url: `${base}${p}`,
    lastModified: new Date(),
    changeFrequency: 'daily' as const,
    priority: p === '' ? 1 : 0.7
  }));

  const [ids, cuisines, categories] = await Promise.all([allRecipeIds(), api.cuisines(), api.categories()]);
  const cuisineRoutes = ((cuisines as any)?.items ?? []).map((c: any) => ({
    url: `${base}/cuisines/${c.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.6
  }));
  const categoryRoutes = ((categories as any)?.items ?? []).map((c: any) => ({
    url: `${base}/categories/${c.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.6
  }));
  const recipeRoutes = ids.map((id) => ({
    url: `${base}/recipes/${id}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: 0.8
  }));

  return [...staticRoutes, ...cuisineRoutes, ...categoryRoutes, ...recipeRoutes];
}
