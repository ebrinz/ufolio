import { ReactNode } from "react";

interface ScrollableChartProps { children: ReactNode; minWidth?: number; className?: string; }

export function ScrollableChart({ children, minWidth = 600, className = "" }: ScrollableChartProps) {
  return (
    <div className={`relative overflow-x-auto -mx-4 px-4 md:mx-0 md:px-0 md:overflow-visible ${className}`}
      style={{ WebkitOverflowScrolling: "touch" }}>
      <div className="pointer-events-none absolute left-0 top-0 bottom-0 w-6 bg-gradient-to-r from-space-900 to-transparent z-10 md:hidden" />
      <div className="pointer-events-none absolute right-0 top-0 bottom-0 w-6 bg-gradient-to-l from-space-900 to-transparent z-10 md:hidden" />
      <div style={{ minWidth }} className="md:!min-w-0">{children}</div>
    </div>
  );
}
