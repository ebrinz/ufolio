"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

interface AnimatedBarProps {
  data: { name: string; value: number }[];
  color?: string;
  horizontal?: boolean;
  height?: number;
  className?: string;
}

export function AnimatedBar({ data, color = "#7aaa88", horizontal = false, height = 400, className = "" }: AnimatedBarProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload?.length) return null;
    return (
      <div className="bg-[#0a0e1a] border border-white/10 rounded px-3 py-2 text-sm">
        <p className="text-[#c8d8cc]">{payload[0].payload.name}</p>
        <p className="text-[#7aaa88] font-mono">{payload[0].value.toLocaleString()}</p>
      </div>
    );
  };

  if (horizontal) {
    return (
      <motion.div ref={ref} initial={{ opacity: 0 }} animate={isInView ? { opacity: 1 } : {}} transition={{ duration: 0.5 }} className={className}>
        <ResponsiveContainer width="100%" height={height}>
          <BarChart data={data} layout="vertical" margin={{ left: 80, right: 40 }}>
            <XAxis type="number" stroke="#333" tick={{ fill: "#666", fontSize: 11 }} />
            <YAxis dataKey="name" type="category" stroke="#333" tick={{ fill: "#999", fontSize: 11 }} width={75} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]} animationDuration={1500}>
              {data.map((_, i) => (<Cell key={i} fill={color} fillOpacity={0.7 + (i / data.length) * 0.3} />))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </motion.div>
    );
  }

  return (
    <motion.div ref={ref} initial={{ opacity: 0 }} animate={isInView ? { opacity: 1 } : {}} transition={{ duration: 0.5 }} className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} margin={{ bottom: 60 }}>
          <XAxis dataKey="name" stroke="#333" tick={{ fill: "#999", fontSize: 11 }} angle={-40} textAnchor="end" />
          <YAxis stroke="#333" tick={{ fill: "#666", fontSize: 11 }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="value" radius={[4, 4, 0, 0]} animationDuration={1500}>
            {data.map((_, i) => (<Cell key={i} fill={color} fillOpacity={0.7 + (i / data.length) * 0.3} />))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
