import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UFOlio — Field Guide to Contact",
  description:
    "A data-driven field guide to UAP encounters, built from 100,000+ reports across 5 independent datasets.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="grain">{children}</body>
    </html>
  );
}
