/** @type {import('next').NextConfig} */
const apiBase = process.env.API_BASE_URL || 'http://127.0.0.1:4000';

const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  compress: true,
  poweredByHeader: false,
  env: { NEXT_PUBLIC_API_BASE: apiBase },
  async headers() {
    return [
      {
        // 静态资源长缓存，HTML 走 CDN/浏览器短缓存
        source: '/_next/static/:path*',
        headers: [{ key: 'cache-control', value: 'public, max-age=31536000, immutable' }]
      },
      {
        source: '/:path*',
        headers: [
          { key: 'x-content-type-options', value: 'nosniff' },
          { key: 'referrer-policy', value: 'strict-origin-when-cross-origin' }
        ]
      }
    ];
  },
  async rewrites() {
    // 浏览器端同源访问 /api/v1/*，服务端直接走 API_BASE_URL
    return [{ source: '/api/v1/:path*', destination: `${apiBase}/api/v1/:path*` }];
  }
};

export default nextConfig;
