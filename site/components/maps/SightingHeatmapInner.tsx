"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { HexCell } from "@/lib/types";

import "leaflet.heat";

interface Props {
  hexCells: HexCell[];
}

export default function SightingHeatmapInner({ hexCells }: Props) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;

    const map = L.map(mapRef.current, {
      center: [39, -98],
      zoom: 4,
      zoomControl: true,
      attributionControl: false,
      scrollWheelZoom: false,
    });

    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
      { maxZoom: 18 }
    ).addTo(map);

    const maxCount = Math.max(...hexCells.map((c) => c.count));
    const heatData = hexCells.map((c) => [c.lat, c.lng, c.count / maxCount]);

    // @ts-expect-error — leaflet.heat
    L.heatLayer(heatData, {
      radius: 15,
      blur: 20,
      maxZoom: 8,
      gradient: {
        0.0: "#020408",
        0.2: "#1a3a2a",
        0.4: "#4a6a52",
        0.6: "#7aaa88",
        0.8: "#c8d8cc",
        1.0: "#ffffff",
      },
    }).addTo(map);

    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, [hexCells]);

  return <div ref={mapRef} className="w-full h-[400px] md:h-[500px]" />;
}
