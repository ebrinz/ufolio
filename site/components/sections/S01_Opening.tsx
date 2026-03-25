"use client";

import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { StatCounter } from "@/components/ui/StatCounter";
import Image from "next/image";

export function S01_Opening() {
  return (
    <section id="opening" className="relative min-h-screen flex flex-col items-center justify-center px-6 starfield">
      <div className="relative z-10 max-w-4xl mx-auto text-center">
        <ScrollReveal delay={0}>
          <Image
            src="/ufolio/banner.svg"
            alt="UFOlio"
            width={700}
            height={296}
            className="mx-auto w-full max-w-[700px] mb-12"
            priority
          />
        </ScrollReveal>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12 mb-16">
          <ScrollReveal delay={0.2}>
            <StatCounter value={102385} label="Reports" suffix="+" />
          </ScrollReveal>
          <ScrollReveal delay={0.4}>
            <StatCounter value={5} label="Datasets" />
          </ScrollReveal>
          <ScrollReveal delay={0.6}>
            <StatCounter value={150} label="Years" suffix="+" />
          </ScrollReveal>
          <ScrollReveal delay={0.8}>
            <StatCounter value={100} label="Countries" suffix="+" />
          </ScrollReveal>
        </div>

        <ScrollReveal delay={1.0}>
          <p className="text-lg md:text-xl lg:text-2xl text-gray-400 font-light leading-relaxed max-w-3xl mx-auto">
            Five unrelated archives, built across different decades by different
            people using different methods, describe{" "}
            <span className="text-[#c8d8cc]">the same phenomenon</span>.
          </p>
        </ScrollReveal>

        <ScrollReveal delay={1.4}>
          <div className="mt-16 animate-bounce text-gray-600">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="mx-auto">
              <path d="M12 5v14M5 12l7 7 7-7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
