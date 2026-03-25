"use client";

import dynamic from "next/dynamic";
import { HexCell } from "@/lib/types";

const MapInner = dynamic(() => import("./SightingHeatmapInner"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[400px] md:h-[500px] bg-[#0f1420] rounded-lg animate-pulse flex items-center justify-center">
      <span className="text-gray-600 font-mono text-sm">Loading map...</span>
    </div>
  ),
});

interface SightingHeatmapProps {
  hexCells: HexCell[];
  className?: string;
}

export function SightingHeatmap({ hexCells, className = "" }: SightingHeatmapProps) {
  return (
    <div className={`rounded-lg overflow-hidden border border-white/5 ${className}`}>
      <MapInner hexCells={hexCells} />
    </div>
  );
}
