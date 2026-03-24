"use client";

import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

interface KDECurveProps {
  data: { logCount: number; frequency: number }[];
  height?: number;
  className?: string;
}

export function KDECurve({ data, height = 250, className = "" }: KDECurveProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <motion.div ref={ref} initial={{ opacity: 0 }} animate={isInView ? { opacity: 1 } : {}} transition={{ duration: 0.8 }} className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="kdeGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#7aaa88" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#7aaa88" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <XAxis dataKey="logCount" stroke="#333" tick={{ fill: "#666", fontSize: 10 }}
            label={{ value: "log₁₀(sightings)", position: "bottom", fill: "#666", fontSize: 11 }} />
          <YAxis stroke="#333" tick={{ fill: "#666", fontSize: 10 }} />
          <Tooltip contentStyle={{ backgroundColor: "#0f1420", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "6px" }} />
          <Area type="monotone" dataKey="frequency" stroke="#7aaa88" fill="url(#kdeGrad)" strokeWidth={2} animationDuration={2000} />
        </AreaChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
