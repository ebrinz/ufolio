import { ReactNode } from "react";

interface CardProps { children: ReactNode; className?: string; hover?: boolean; }

export function Card({ children, className = "", hover = true }: CardProps) {
  return (
    <div className={`rounded-lg border border-white/5 bg-white/[0.02] backdrop-blur-sm p-5 md:p-6 ${hover ? "transition-colors hover:bg-white/[0.04] hover:border-accent/20" : ""} ${className}`}>
      {children}
    </div>
  );
}
