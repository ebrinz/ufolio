"use client";
import { useScrollProgress } from "@/lib/useScrollProgress";

export function ProgressBar() {
  const progress = useScrollProgress();
  return (
    <div className="fixed top-0 left-0 right-0 z-50 h-[2px] bg-space-800">
      <div className="h-full bg-accent/60 transition-[width] duration-100" style={{ width: `${progress * 100}%` }} />
    </div>
  );
}
