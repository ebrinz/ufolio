"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

interface StackedBarProps {
  data: Record<string, any>[];
  keys: string[];
  colors: string[];
  xKey: string;
  height?: number;
  className?: string;
}

export function StackedBar({ data, keys, colors, xKey, height = 350, className = "" }: StackedBarProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <motion.div ref={ref} initial={{ opacity: 0, y: 20 }} animate={isInView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6 }} className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data}>
          <XAxis dataKey={xKey} stroke="#333" tick={{ fill: "#999", fontSize: 11 }} />
          <YAxis stroke="#333" tick={{ fill: "#666", fontSize: 11 }} />
          <Tooltip contentStyle={{ backgroundColor: "#0f1420", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "6px", fontSize: "12px" }} />
          <Legend wrapperStyle={{ fontSize: "11px", color: "#999" }} />
          {keys.map((key, i) => (
            <Bar key={key} dataKey={key} stackId="stack" fill={colors[i % colors.length]} fillOpacity={0.8} animationDuration={1500} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
