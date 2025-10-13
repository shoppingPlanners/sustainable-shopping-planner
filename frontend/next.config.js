/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/brands/:path*',
        destination: 'http://localhost:5001/:path*',
      },
      {
        source: '/api/ratings/:path*',
        destination: 'http://localhost:5002/:path*',
      },
      {
        source: '/api/behavior/:path*',
        destination: 'http://localhost:5003/:path*',
      },
      {
        source: '/api/suggestions/:path*',
        destination: 'http://localhost:5004/:path*',
      },
    ]
  },
}

module.exports = nextConfig

