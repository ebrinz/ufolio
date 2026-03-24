import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/ufolio",
  images: { unoptimized: true },
};

export default nextConfig;
