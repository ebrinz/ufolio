import { ProgressBar } from "@/components/ui/ProgressBar";
import { SectionNav } from "@/components/ui/SectionNav";
import { S01_Opening } from "@/components/sections/S01_Opening";

export default function Home() {
  return (
    <>
      <ProgressBar />
      <SectionNav />
      <main className="pb-20 lg:pb-0">
        <S01_Opening />

        {/* Encounter sections coming next */}
        <section className="py-32 text-center text-gray-600">
          <p className="font-mono text-sm tracking-wider">
            Encounter data sections loading...
          </p>
        </section>
      </main>
    </>
  );
}
