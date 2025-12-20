/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'export',
  // images: {
  //   unoptimized: true,
  // },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination:
          'https://love-in-paradise-api-production.up.railway.app/api/home/:path*',
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/',
        headers: [
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
