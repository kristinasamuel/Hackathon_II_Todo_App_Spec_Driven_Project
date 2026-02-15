/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true, // Recommended for Next.js
  swcMinify: true,
  experimental: {
    // Disable Turbopack explicitly as requested
    // This is often not needed in production but can help resolve development warnings
    // For turbopack.root, we use path.join(__dirname) to correctly resolve the current directory
    // turbopack: {
    //   enabled: false,
    //   root: path.join(__dirname), // Ensure the correct root is inferred
    // },
  },
  // If you are using any local packages or packages that require transpilation
  // (e.g., specific AI libraries that might not be pre-compiled for browser)
  // you might need to add them here. Example:
  // transpilePackages: ["@google/gemini-pro"],
  // Images configuration for Vercel deployment
  images: {
    domains: ['lh3.googleusercontent.com', 'avatars.githubusercontent.com'],
  },
};

module.exports = nextConfig;