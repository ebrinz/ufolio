"use client";
import { useAnimatedCounter } from "@/lib/useAnimatedCounter";
import { useInView } from "framer-motion";
import { useRef } from "react";

interface StatCounterProps {
  value: number;
  label: string;
  suffix?: string;
  prefix?: string;
  className?: string;
  duration?: number;
}

export function StatCounter({ value, label, suffix = "", prefix = "", className = "", duration = 2000 }: StatCounterProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });
  const count = useAnimatedCounter(value, duration, isInView);
  return (
    <div ref={ref} className={`text-center ${className}`}>
      <div className="font-mono text-4xl md:text-5xl lg:text-6xl font-light text-accent-light tracking-wide">
        {prefix}{count.toLocaleString()}{suffix}
      </div>
      <div className="mt-2 text-sm md:text-base text-gray-400 tracking-wider uppercase">{label}</div>
    </div>
  );
}
