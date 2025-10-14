/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: "/",
        destination: "/home",
        permanent: true,
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/api/(.*)",
        destination: "/api/index.py",
      },
    ];
  },
};

export default nextConfig;
