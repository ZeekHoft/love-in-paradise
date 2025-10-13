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
        source: "/api/home",
        destination: "/api/app.py",
      },
    ];
  },
};

export default nextConfig;
