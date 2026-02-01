import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  async rewrites() {
    return [
      {
        source: '/predict/:path*',
        destination: 'http://localhost:8000/predict/:path*',
      },
      {
        source: '/simulate/:path*',
        destination: 'http://localhost:8000/simulate/:path*',
      },
      {
        source: '/analyze/:path*',
        destination: 'http://localhost:8000/analyze/:path*',
      },
    ];
  },
};

export default nextConfig;
