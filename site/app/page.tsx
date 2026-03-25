import { ProgressBar } from "@/components/ui/ProgressBar";
import { SectionNav } from "@/components/ui/SectionNav";
import { S01_Opening } from "@/components/sections/S01_Opening";
import { S02_Shapes } from "@/components/sections/S02_Shapes";
import { S03_Geography } from "@/components/sections/S03_Geography";

export default function Home() {
  return (
    <>
      <ProgressBar />
      <SectionNav />
      <main className="pb-20 lg:pb-0">
        <S01_Opening />
        <S02_Shapes />
        <S03_Geography />

        {/* Placeholder for remaining sections */}
        <section className="py-32 text-center text-gray-600">
          <p className="font-mono text-sm tracking-wider">
            Sections 4–15 coming in Phases 2–4
          </p>
        </section>
      </main>
    </>
  );
}
