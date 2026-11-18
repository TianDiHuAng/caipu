import Link from 'next/link';
import type { RecipeSummary } from '@/lib/api';
import { dictFor } from '@/lib/i18n';
import { getLocale } from '@/lib/locale-server';

/**
 * 搜索关键词高亮：只做纯文本切分，不使用 dangerouslySetInnerHTML，避免 XSS。
 * 命中的片段按原顺序拼接，保证长文本也能正确还原。
 */
export function Highlight({ text, q }: { text: string; q?: string }) {
  const term = (q ?? '').trim();
  if (!term || !text) return <>{text}</>;
  const lower = text.toLowerCase();
  const needle = term.toLowerCase();
  const parts: React.ReactNode[] = [];
  let from = 0;
  let hit = lower.indexOf(needle);
  while (hit !== -1) {
    if (hit > from) parts.push(text.slice(from, hit));
    parts.push(
      <mark key={`${hit}-${parts.length}`} className="bg-yellow-200 px-0.5">
        {text.slice(hit, hit + needle.length)}
      </mark>
    );
    from = hit + needle.length;
    hit = lower.indexOf(needle, from);
  }
  if (from < text.length) parts.push(text.slice(from));
  return <>{parts}</>;
}

const flavorZh: Record<string, string> = {
  salty: '咸', sweet: '甜', sour: '酸', spicy: '辣', numbing: '麻', bitter: '苦', umami: '鲜',
  light: '清淡', rich: '浓香', fragrant: '香', smoky: '烟熏', herbal: '香草'
};

const categoryZh: Record<string, string> = {
  appetizer: '前菜', salad: '沙拉', soup: '汤羹', 'main-meat': '主菜·肉', 'main-poultry': '主菜·禽',
  'main-seafood': '主菜·海鲜', 'main-egg': '主菜·蛋', 'main-tofu': '主菜·豆制品',
  'main-vegetable': '主菜·蔬菜', 'staple-rice': '主食·饭', 'staple-noodle': '主食·面',
  'staple-bread': '主食·饼', congee: '粥', 'street-food': '小吃', bakery: '烘焙',
  dessert: '甜点', drink: '饮品', sauce: '酱汁', fermented: '腌制发酵', breakfast: '早餐',
  'kids': '儿童餐', banquet: '宴客菜', 'healthy': '低卡健身', 'special-diet': '特殊饮食',
  'hotpot': '火锅烧烤', 'cold-dish': '凉菜'
};

export function RecipeCard({ r, q }: { r: RecipeSummary; q?: string }) {
  const locale = getLocale();
  const t = dictFor(locale);
  const enFirst = locale === 'en';
  const name = (enFirst ? r.name?.en ?? r.name?.zh : r.name?.zh ?? r.name?.en) ?? r.id;
  const sub = enFirst ? r.name?.zh : r.name?.en;
  const total = r.total_min ?? r.time?.total_min;
  return (
    <article className="rounded-lg border border-slate-200 p-4 transition hover:border-brand-500 hover:shadow-sm">
      <h3 className="text-base font-semibold">
        <Link href={`/recipes/${r.id}`} className="no-underline text-slate-800 hover:text-brand-600">
          <Highlight text={name} q={q} />
        </Link>
      </h3>
      {sub ? <p className="mt-0.5 text-xs text-slate-500">{sub}</p> : null}
      <p className="mt-2 flex flex-wrap gap-2 text-xs text-slate-600">
        <span className="rounded bg-brand-50 px-1.5 py-0.5 text-brand-700">
          {t('difficulty')} {r.difficulty}/5
        </span>
        {total ? (
          <span className="rounded bg-slate-100 px-1.5 py-0.5">
            {total} {t('minutes')}
          </span>
        ) : null}
        {(r.category ?? []).slice(0, 2).map((c) => (
          <span key={c} className="rounded bg-slate-100 px-1.5 py-0.5">
            {enFirst ? String(c).replace(/-/g, ' ') : categoryZh[c] ?? c}
          </span>
        ))}
      </p>
      {(r.flavor ?? []).length ? (
        <p className="mt-1 text-xs text-slate-500">
          {enFirst ? t('flavor') : `口味`}：
          {(r.flavor ?? []).map((f) => (enFirst ? f : flavorZh[f] ?? f)).join(' / ')}
        </p>
      ) : null}
    </article>
  );
}

export function RecipeGrid({ items, q }: { items: RecipeSummary[]; q?: string }) {
  const t = dictFor(getLocale());
  if (!items.length) return <p className="text-slate-500">{t('empty')}</p>;
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((r) => (
        <RecipeCard key={r.id} r={r} q={q} />
      ))}
    </div>
  );
}

export function Pagination({ total, page, pageSize, basePath }: { total: number; page: number; pageSize: number; basePath: string }) {
  const t = dictFor(getLocale());
  const pages = Math.max(1, Math.ceil(total / pageSize));
  if (pages <= 1) return null;
  const link = (p: number) => (p === 1 ? basePath : `${basePath}${basePath.includes('?') ? '&' : '?'}page=${p}`);
  return (
    <nav aria-label="分页" className="mt-6 flex items-center gap-3 text-sm">
      {page > 1 ? <Link href={link(page - 1)}>{t('prev')}</Link> : <span className="text-slate-400">{t('prev')}</span>}
      <span className="text-slate-600">
        {page} / {pages} {t('pageInfo')} · {t('totalRecipes')} {total}
      </span>
      {page < pages ? <Link href={link(page + 1)}>{t('next')}</Link> : <span className="text-slate-400">{t('next')}</span>}
    </nav>
  );
}

export { flavorZh, categoryZh };
