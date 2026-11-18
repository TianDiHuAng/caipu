import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/api';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/', disallow: ['/recipes/*/print'] }],
    sitemap: `${SITE.url}/sitemap.xml`,
    host: SITE.url
  };
}
