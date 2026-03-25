"use client";

import { SectionHeader } from "@/components/ui/SectionHeader";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { Card } from "@/components/ui/Card";
import { SourceTag } from "@/components/ui/SourceTag";
import { ScrollableChart } from "@/components/ui/ScrollableChart";
import { AnimatedBar } from "@/components/charts/AnimatedBar";
import { StackedBar } from "@/components/charts/StackedBar";
import { KDECurve } from "@/components/charts/KDECurve";
import type { NuforcShapes } from "@/lib/types";

import shapesData from "@/data/nuforc-shapes.json";

const data = shapesData as NuforcShapes;

export function S02_Shapes() {
  const barData = data.topShapes.map((s) => ({ name: s.shape, value: s.count }));

  const regionKeys = Object.keys(data.regionBreakdown[0]?.shapes || {});
  const regionData = data.regionBreakdown.map((r) => ({ region: r.region, ...r.shapes }));
  const regionColors = ["#7aaa88", "#f5d442", "#06b6d4", "#a855f7", "#f59e0b"];

  return (
    <section id="shapes" className="py-24 md:py-32 px-6 max-w-6xl mx-auto">
      <SectionHeader number={2} title="The Scale of Sightings" subtitle="What people see in the sky" />

      <ScrollReveal>
        <Card className="mb-12 max-w-xl">
          <p className="text-gray-400">
            The top 3 shapes —{" "}
            <span className="text-[#c8d8cc]">light</span>,{" "}
            <span className="text-[#c8d8cc]">triangle</span>, and{" "}
            <span className="text-[#c8d8cc]">circle</span> — account for{" "}
            <span className="text-3xl font-mono text-[#c8d8cc]">{data.topThreePercent}%</span>{" "}
            of all {data.totalRecords.toLocaleString()} reports.
          </p>
          <SourceTag source="NUFORC" detail={`n=${data.totalRecords.toLocaleString()}`} />
        </Card>
      </ScrollReveal>

      <ScrollReveal>
        <h3 className="text-lg text-gray-400 mb-4 font-mono">Top 15 Reported Shapes</h3>
        <ScrollableChart minWidth={700}>
          <AnimatedBar data={barData} horizontal height={500} />
        </ScrollableChart>
      </ScrollReveal>

      <ScrollReveal className="mt-16">
        <h3 className="text-lg text-gray-400 mb-4 font-mono">Shape Mix by Region</h3>
        <p className="text-sm text-gray-500 mb-6">The distribution is remarkably consistent across regions — light dominates everywhere.</p>
        <ScrollableChart>
          <StackedBar data={regionData} keys={regionKeys} colors={regionColors} xKey="region" height={300} />
        </ScrollableChart>
        <SourceTag source="NUFORC" detail="US only, top 5 shapes × 4 Census regions" />
      </ScrollReveal>

      <ScrollReveal className="mt-16">
        <h3 className="text-lg text-gray-400 mb-4 font-mono">The Power Law</h3>
        <p className="text-sm text-gray-500 mb-6">Shape frequency follows a steep power law — a few categories dominate while most are rare. On a log scale, the distribution reveals a smooth curve rather than random noise.</p>
        <KDECurve data={data.distributionCurve} />
        <SourceTag source="NUFORC" detail="log₁₀ shape counts, KDE smoothed" />
      </ScrollReveal>
    </section>
  );
}
