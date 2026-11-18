import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * 语言切换：?lang=en|zh 优先，其次读 cookie。
 * 通过请求头把结果传给服务端组件，保证「点了切换当次响应就是目标语言」，
 * 不跳转、不改地址，避免破坏现有链接的 SEO 收录。
 */
export function middleware(req: NextRequest) {
  const fromQuery = req.nextUrl.searchParams.get('lang');
  const fromCookie = req.cookies.get('lang')?.value;
  const locale = (fromQuery ?? fromCookie) === 'en' ? 'en' : 'zh';

  const headers = new Headers(req.headers);
  headers.set('x-locale', locale);

  const res = NextResponse.next({ request: { headers } });
  if (fromQuery === 'en' || fromQuery === 'zh') {
    res.cookies.set('lang', fromQuery, { path: '/', maxAge: 60 * 60 * 24 * 365, sameSite: 'lax' });
  }
  return res;
}

export const config = {
  matcher: ['/((?!_next|api|favicon.ico).*)']
};
