"use client";
import { useState, useEffect } from "react";
import { SECTIONS } from "@/lib/types";
import { motion, AnimatePresence } from "framer-motion";

export function SectionNav() {
  const [activeSection, setActiveSection] = useState("opening");
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => { const visible = entries.find((e) => e.isIntersecting); if (visible) setActiveSection(visible.target.id); },
      { rootMargin: "-40% 0px -40% 0px" }
    );
    SECTIONS.forEach((s) => { const el = document.getElementById(s.id); if (el) observer.observe(el); });
    return () => observer.disconnect();
  }, []);

  const active = SECTIONS.find((s) => s.id === activeSection);
  const scrollTo = (id: string) => { document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); setIsOpen(false); };

  return (
    <>
      <nav className="hidden lg:flex fixed right-4 top-1/2 -translate-y-1/2 z-40 flex-col gap-2">
        {SECTIONS.map((s) => (
          <button key={s.id} onClick={() => scrollTo(s.id)}
            className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${s.id === activeSection ? "bg-accent scale-125" : "bg-white/20 hover:bg-white/40"}`}
            title={s.title} />
        ))}
      </nav>
      <div className="lg:hidden fixed bottom-0 left-0 right-0 z-40">
        <AnimatePresence>
          {isOpen && (
            <motion.div initial={{ y: "100%" }} animate={{ y: 0 }} exit={{ y: "100%" }} transition={{ type: "spring", damping: 25 }}
              className="bg-space-700/95 backdrop-blur-md border-t border-white/10 max-h-[60vh] overflow-y-auto">
              {SECTIONS.map((s) => (
                <button key={s.id} onClick={() => scrollTo(s.id)}
                  className={`w-full text-left px-5 py-3 text-sm flex items-center gap-3 ${s.id === activeSection ? "text-accent bg-white/5" : "text-gray-400"}`}>
                  <span className="font-mono text-xs text-accent-dim w-5">{String(s.number).padStart(2, "0")}</span>
                  {s.title}
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
        <button onClick={() => setIsOpen(!isOpen)}
          className="w-full bg-space-800/95 backdrop-blur-md border-t border-white/10 px-5 py-3 flex items-center justify-between">
          <span className="text-sm text-gray-400">
            <span className="font-mono text-accent-dim mr-2">{String(active?.number ?? 1).padStart(2, "0")}</span>
            {active?.title}
          </span>
          <span className="text-accent text-xs">{isOpen ? "▼" : "▲"}</span>
        </button>
      </div>
    </>
  );
}
