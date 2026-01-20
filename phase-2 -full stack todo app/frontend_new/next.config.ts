import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable experimental SWC minification for better performance
  swcMinify: true,

  // Optimize images if you plan to use them
  images: {
    domains: ['localhost', 'your-backend-domain.vercel.app'], // Add your Vercel domain here
  },

  // Additional configuration for Vercel deployment
  async rewrites() {
    return [
      // This is needed for API proxying if needed
      // {
      //   source: '/api/:path*',
      //   destination: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/:path*`,
      // },
    ];
  },

  // For static export, uncomment the following:
  // output: 'export',
  // trailingSlash: true,
  // images: {
  //   unoptimized: true,
  // },
};

export default nextConfig;
