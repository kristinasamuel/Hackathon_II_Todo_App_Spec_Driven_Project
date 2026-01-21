import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // ✅ swcMinify is automatic in new Next.js versions
  // (removed to fix "Unrecognized key" warning)

  // ✅ Updated image config (domains → remotePatterns)
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
      },
      {
        protocol: "https",
        hostname: "your-backend-domain.vercel.app", // replace with real backend domain
      },
    ],
  },

  // ✅ Rewrites kept clean (no invalid config)
  async rewrites() {
    return [
      // Uncomment ONLY if you really need API proxying
      // {
      //   source: "/api/:path*",
      //   destination: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/:path*`,
      // },
    ];
  },

  // ✅ Optional: prevents turbopack root warning
  turbopack: {
    root: "./",
  },
};

export default nextConfig;
