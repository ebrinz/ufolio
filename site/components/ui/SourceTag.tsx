interface SourceTagProps { source: string; detail?: string; }

export function SourceTag({ source, detail }: SourceTagProps) {
  return (
    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] md:text-xs font-mono bg-white/5 text-gray-500 border border-white/5">
      <span className="text-accent-dim">{source}</span>
      {detail && <span className="text-gray-600">· {detail}</span>}
    </span>
  );
}
