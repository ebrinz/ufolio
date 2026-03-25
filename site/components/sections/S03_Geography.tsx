"use client";

import { SectionHeader } from "@/components/ui/SectionHeader";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { Card } from "@/components/ui/Card";
import { SourceTag } from "@/components/ui/SourceTag";
import { SightingHeatmap } from "@/components/maps/SightingHeatmap";
import type { NuforcGeo, ConcentrationRatio } from "@/lib/types";

import geoData from "@/data/nuforc-geo.json";

const data = geoData as NuforcGeo;

function ConcentrationTable({ ratios }: { ratios: ConcentrationRatio[] }) {
  const overRep = ratios.filter((r) => r.ratio > 1).slice(0, 10);
  const underRep = ratios.filter((r) => r.ratio < 1).slice(0, 5);

  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div>
        <h4 className="text-sm font-mono text-[#4a6a52] mb-3 tracking-wider">OVER-REPRESENTED</h4>
        <div className="space-y-2">
          {overRep.map((r, i) => (
            <div key={i} className="flex items-center justify-between text-sm bg-white/[0.02] rounded px-3 py-2">
              <span className="text-gray-300"><span className="text-[#c8d8cc]">{r.shape}</span> in {r.region}</span>
              <span className="font-mono text-[#7aaa88]">{r.ratio.toFixed(2)}x</span>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h4 className="text-sm font-mono text-[#4a6a52] mb-3 tracking-wider">UNDER-REPRESENTED</h4>
        <div className="space-y-2">
          {underRep.map((r, i) => (
            <div key={i} className="flex items-center justify-between text-sm bg-white/[0.02] rounded px-3 py-2">
              <span className="text-gray-300"><span className="text-[#c8d8cc]">{r.shape}</span> in {r.region}</span>
              <span className="font-mono text-gray-500">{r.ratio.toFixed(2)}x</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function S03_Geography() {
  return (
    <section id="geography" className="py-24 md:py-32 px-6 max-w-6xl mx-auto">
      <SectionHeader number={3} title="The Geography of Lights" subtitle="Where sightings cluster" />

      <ScrollReveal>
        <p className="text-sm text-gray-500 mb-4">
          {data.hexCells.length.toLocaleString()} grid cells aggregated from 65,000+ US sightings. Density broadly mirrors population — but the anomalies are in the details.
        </p>
        <SightingHeatmap hexCells={data.hexCells} />
        <div className="mt-2">
          <SourceTag source="NUFORC" detail="US lat/lon, 0.25° hexbin" />
        </div>
      </ScrollReveal>

      <ScrollReveal className="mt-12">
        <Card className="border-[#7aaa88]/20 max-w-2xl">
          <p className="text-lg text-gray-300">&ldquo;{data.topInsight}&rdquo;</p>
          <p className="mt-3 text-sm text-gray-500">
            Witnesses in the Pacific Northwest are significantly more likely to report something they cannot categorize. This could mean more cautious reporters — or genuinely unusual sightings.
          </p>
          <SourceTag source="NUFORC" detail="χ² test, p < 0.001" />
        </Card>
      </ScrollReveal>

      <ScrollReveal className="mt-12">
        <h3 className="text-lg text-gray-400 mb-2 font-mono">Shape × Region Anomalies</h3>
        <p className="text-sm text-gray-500 mb-6">
          Concentration ratio: a region&apos;s share of a shape ÷ its share of all sightings. Values above 1.0 = over-represented; below 1.0 = under-represented. Only statistically significant results shown (p &lt; 0.05).
        </p>
        <ConcentrationTable ratios={data.concentrationRatios} />
        <div className="mt-4">
          <SourceTag source="NUFORC" detail="chi-squared, shapes ≥100 reports" />
        </div>
      </ScrollReveal>
    </section>
  );
}
