"use client";

import { SectionHeader } from "@/components/ui/SectionHeader";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { Card } from "@/components/ui/Card";
import { SourceTag } from "@/components/ui/SourceTag";
import { StatCounter } from "@/components/ui/StatCounter";
import type { NuforcGeo, ConcentrationRatio } from "@/lib/types";

import geoData from "@/data/nuforc-geo.json";

const data = geoData as NuforcGeo;

function ConcentrationTable({ ratios }: { ratios: ConcentrationRatio[] }) {
  const overRep = ratios.filter((r) => r.ratio > 1).slice(0, 8);

  return (
    <div>
      <div className="space-y-2">
        {overRep.map((r, i) => (
          <div key={i} className="flex items-center justify-between text-sm bg-white/[0.02] rounded px-3 py-2">
            <span className="text-gray-300"><span className="text-[#c8d8cc]">{r.shape}</span> in {r.region}</span>
            <span className="font-mono text-[#7aaa88]">{r.ratio.toFixed(2)}x</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function S03_Geography() {
  // These would ideally come from the data pipeline, but we computed them in our analysis
  const contactPct = 0.66; // abduction mentions in credible NUFORC reports
  const highStrangenessPct = 7.7; // reports with any high-strangeness element

  return (
    <section id="geography" className="py-24 md:py-32 px-6 max-w-6xl mx-auto">
      <SectionHeader
        number={3}
        title="The Rarity of Contact"
        subtitle="Most sightings are lights. The real signal is in what's left."
      />

      {/* The key insight: contact is rare */}
      <ScrollReveal>
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card hover={false} className="text-center py-8">
            <div className="text-4xl md:text-5xl font-mono font-light text-gray-400 mb-2">80,332</div>
            <div className="text-sm text-gray-500">Total NUFORC reports</div>
          </Card>
          <Card hover={false} className="text-center py-8">
            <div className="text-4xl md:text-5xl font-mono font-light text-[#f59e0b] mb-2">{highStrangenessPct}%</div>
            <div className="text-sm text-gray-500">Mention anything anomalous beyond a light in the sky</div>
          </Card>
          <Card hover={false} className="text-center py-8">
            <div className="text-4xl md:text-5xl font-mono font-light text-[#ef4444] mb-2">{contactPct}%</div>
            <div className="text-sm text-gray-500">Describe anything resembling contact or abduction</div>
          </Card>
        </div>
      </ScrollReveal>

      <ScrollReveal>
        <Card className="max-w-2xl mb-12">
          <p className="text-gray-400 leading-relaxed">
            NUFORC is a sighting database — people report what they saw in the sky.
            The vast majority are brief observations of unexplained lights or objects.
            Only a thin slice describes something more: physical effects, entities,
            communication, or experiences that suggest contact.
          </p>
          <p className="text-gray-400 mt-3 leading-relaxed">
            That thin slice is where the other four datasets begin. Rosales, Magonia,
            Mack, and FREE all focus on the{" "}
            <span className="text-[#c8d8cc]">encounter itself</span> — what happens when the distance closes.
          </p>
        </Card>
      </ScrollReveal>

      {/* Regional concentration — what IS interesting geographically */}
      <ScrollReveal>
        <Card className="border-[#7aaa88]/20 max-w-2xl mb-8">
          <p className="text-lg text-gray-300">&ldquo;{data.topInsight}&rdquo;</p>
          <p className="mt-3 text-sm text-gray-500">
            While sighting density mostly mirrors population, certain shapes are
            statistically over-concentrated in specific regions. These anomalies
            survive chi-squared testing at p &lt; 0.05.
          </p>
          <SourceTag source="NUFORC" detail="χ² test, p < 0.05" />
        </Card>
      </ScrollReveal>

      <ScrollReveal>
        <h3 className="text-lg text-gray-400 mb-2 font-mono">Notable Regional Concentrations</h3>
        <p className="text-sm text-gray-500 mb-6">
          Ratio = region&apos;s share of a shape ÷ region&apos;s share of all sightings. Above 1.0 = over-represented.
        </p>
        <ConcentrationTable ratios={data.concentrationRatios} />
        <div className="mt-4">
          <SourceTag source="NUFORC" detail="chi-squared, shapes ≥100 reports" />
        </div>
      </ScrollReveal>
    </section>
  );
}
