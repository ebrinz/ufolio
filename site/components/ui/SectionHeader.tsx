import { ScrollReveal } from "./ScrollReveal";

interface SectionHeaderProps { number: number; title: string; subtitle?: string; }

export function SectionHeader({ number, title, subtitle }: SectionHeaderProps) {
  return (
    <ScrollReveal className="mb-12 md:mb-16">
      <div className="text-accent-dim font-mono text-sm tracking-[0.3em] mb-3">{String(number).padStart(2, "0")}</div>
      <h2 className="text-2xl md:text-4xl lg:text-5xl font-light text-accent-light tracking-wide leading-tight">{title}</h2>
      {subtitle && <p className="mt-3 text-base md:text-lg text-gray-500 max-w-2xl">{subtitle}</p>}
    </ScrollReveal>
  );
}
