import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          900: "#020408",
          800: "#060a14",
          700: "#0a0e1a",
          600: "#0f1420",
          500: "#1a2030",
        },
        accent: {
          DEFAULT: "#7aaa88",
          light: "#c8d8cc",
          dim: "#4a6a52",
        },
        entity: {
          grey: "#808080",
          nordic: "#f5d442",
          reptilian: "#22c55e",
          insectoid: "#a855f7",
          robotic: "#94a3b8",
          luminous: "#06b6d4",
          human: "#3b82f6",
        },
        warn: "#f59e0b",
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"Fira Code"', '"SF Mono"', "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
