# UFOlio Field Guide — Scrollable Infographic Design Spec

## Overview

A single-page, scroll-driven data infographic built with Next.js and deployed to GitHub Pages. The site presents UFO/UAP encounter data from 5 datasets as a narrative "Field Guide to Contact" — practical, well-sourced, and data-driven.

**Framing:** The Field Guide (B) is the product. The Convergence thesis (C) provides the rationale. The Evidence Map (A) provides the supporting data layer. Every section earns its place by building toward practical utility.

**Audience:** Mixed — informed curious, researchers, and experiencers. The narrative carries the curious reader, the data layer satisfies the researcher, and the entity/experience taxonomy validates the experiencer.

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Framework | Next.js 14 (App Router) | Static export for GitHub Pages |
| Styling | Tailwind CSS | Dark theme, mobile-first responsive |
| Animations | Framer Motion | `whileInView` scroll triggers, Safari-safe |
| Charts | Recharts | React-native, `ResponsiveContainer`, diverse chart types |
| Maps | React-Leaflet + Leaflet | No API key, lightweight, Safari-compatible |
| Data | Pre-computed JSON | Python pipeline → JSON bundles at build time |
| Deployment | GitHub Pages | `output: 'export'` static HTML |

## Architecture

```
ufolio/
├── site/                          ← Next.js app
│   ├── app/
│   │   ├── layout.tsx             ← dark theme, fonts, metadata
│   │   ├── page.tsx               ← section orchestrator
│   │   └── globals.css            ← tailwind + custom CSS
│   ├── components/
│   │   ├── sections/              ← one component per chapter (01-15)
│   │   ├── charts/                ← AnimatedBar, AnimatedLine, Donut, Heatmap, etc.
│   │   ├── maps/                  ← SightingHeatmap, EncounterClusters, etc.
│   │   └── ui/                    ← ScrollReveal, StatCounter, Card, ProgressBar, etc.
│   ├── data/                      ← pre-computed JSON bundles
│   │   ├── nuforc-shapes.json
│   │   ├── nuforc-geo.json
│   │   ├── rosales-entities.json
│   │   ├── rosales-timeline.json
│   │   ├── magonia-summary.json
│   │   ├── mack-cases.json
│   │   ├── free-findings.json
│   │   ├── entity-taxonomy.json
│   │   ├── high-strangeness.json
│   │   ├── convergence.json
│   │   └── encounter-settings.json
│   ├── public/
│   │   ├── media/                 ← static images, entity silhouettes
│   │   └── banner.svg
│   └── lib/
│       ├── useScrollReveal.ts     ← intersection observer hook
│       ├── useAnimatedCounter.ts  ← number counting animation
│       └── types.ts               ← shared TypeScript types
├── scripts/
│   └── build-site-data.py         ← reads all CSVs/JSONs → site/data/*.json
└── [existing dataset directories]
```

### Data Pipeline

`scripts/build-site-data.py` runs before the Next.js build. It:
1. Reads all 5 dataset CSV/JSON files
2. Computes all aggregations (shape counts, entity taxonomy, geographic clusters, timeline data, cross-dataset correlations)
3. Outputs compact JSON bundles to `site/data/`
4. Keeps bundle sizes small — pre-aggregated, no raw records shipped to client

### Responsive Strategy

- **Mobile-first**: design for 375px, enhance upward
- **Breakpoints**: `sm:640px`, `md:768px`, `lg:1024px`, `xl:1280px`
- **Charts**: `ResponsiveContainer` wraps all Recharts; simplified series on mobile
- **Maps**: full-width on mobile, simplified controls, pinch-to-zoom
- **Scroll animations**: same `whileInView` triggers; no parallax on mobile (fights iOS momentum)
- **Typography**: fluid type scale using `clamp()`
- **Touch**: all interactive elements have 44px minimum tap targets

## Sections (15 Chapters)

### Section 1: "The Signal in the Noise"
- **Purpose**: Hook. Establish scale. State convergence thesis.
- **Visuals**: Animated counters (102K reports, 5 datasets, 150 years, 100+ countries). Starfield CSS background. Banner aliens.
- **Data**: Hardcoded counts from all datasets.
- **Mobile**: Counters stack vertically.

### Section 2: "The Scale of Sightings"
- **Purpose**: NUFORC baseline. Most reports are lights. Establish "normal."
- **Visuals**: Animated bar chart (top 15 shapes, bars grow on scroll). Small multiples (4 regional stacked bars). Power-law KDE curve.
- **Data**: `nuforc-shapes.json` — shape counts, regional breakdowns, distribution curve points.
- **Key stat**: "Top 3 shapes = 39.9% of all reports"
- **Mobile**: Bar chart horizontal/scrollable, small multiples 2×2.

### Section 3: "The Geography of Lights"
- **Purpose**: Where sightings cluster. Population mirror + anomalies.
- **Visuals**: Leaflet heatmap (65K US lat/lon). Concentration ratio table (shape × region). Toggle: pop density vs. sighting density.
- **Data**: `nuforc-geo.json` — lat/lon points (downsampled for performance), concentration ratios.
- **Key insight**: "PNW's signature isn't a shape — it's 'unknown' at 1.34x"
- **Mobile**: Map full-width, table → swipeable cards.

### Section 4: "When It Gets Close"
- **Purpose**: Transition sightings → encounters. NUFORC ends, Rosales/Magonia begin.
- **Visuals**: Visual progression (Sighting → Close Encounter → Contact). Donut chart (Rosales type codes). Decade timeline bar chart.
- **Data**: `rosales-timeline.json` — type code counts, volume by decade.
- **Key insight**: "41.6% are Type E — entity without a UFO. The being is the event."
- **Mobile**: Donut → horizontal stacked bar, timeline vertical.

### Section 5: "The Census of Visitors"
- **Purpose**: Entity taxonomy. Core of the field guide.
- **Visuals**: Grid of entity types with silhouette icons, count badges, prevalence bars. Tap/hover for description + sample excerpt.
- **Data**: `entity-taxonomy.json` — 32 entity types with counts across Rosales/Magonia/NUFORC, sample descriptions.
- **Mobile**: Grid → scrollable card list, tap to expand.

### Section 6: "The Shift"
- **Purpose**: Entity types changing over time. What does it mean?
- **Visuals**: Animated line chart (entity prevalence by decade, 1940s–2000s). Annotated transitions.
- **Data**: `rosales-timeline.json` — entity type percentages per decade.
- **Key insight**: "Nordics collapsing. Greys rising. Reptilians emerging."
- **Mobile**: Fewer series with toggle, annotations as scroll cards below chart.

### Section 7: "The Ones Who Look Like Us"
- **Purpose**: The 3.7% that could pass. Most practical section.
- **Visuals**: Three profile cards (Nordic, Human-Looking, MIB). Passability scorecard. Behavior comparison bar chart. "The Tells" checklist.
- **Data**: `entity-taxonomy.json` — human-passing subset with behavioral stats.
- **Mobile**: Cards stack, scorecard → vertical list, excerpts in accordions.

### Section 8: "Where They Show Up"
- **Purpose**: Encounter settings. Practical patterns.
- **Visuals**: Treemap or horizontal bar (settings breakdown). Map overlay (encounter clusters). Cross-reference callouts (military 1.4x, water 1.4x).
- **Data**: `encounter-settings.json` — setting percentages, geographic clusters, cross-references.
- **Mobile**: Treemap → horizontal bar, map full-width.

### Section 9: "What Happens to Your Body"
- **Purpose**: Physical effects. Measurable consequences.
- **Visuals**: Icon grid (EMF, vehicle stall, burns, nausea, sound). Prevalence stats. Co-occurrence chart. FREE healing callout (50%).
- **Data**: `high-strangeness.json` — physical effect counts, co-occurrence matrix, FREE stats.
- **Key stat**: "Military presence reports: highest credibility score (1.9 avg)"
- **Mobile**: Icon grid 2-column.

### Section 10: "What Happens to Your Mind"
- **Purpose**: Consciousness/psi. FREE survey central.
- **Visuals**: Large animated stat callouts (78% telepathy, 80% OBE, 36% NDE, 85% positive). Psi subcategory breakdown. Mack case study cards (14). Timeline of psi mentions.
- **Data**: `free-findings.json` — all 45 aggregate findings. `mack-cases.json` — 14 case summaries.
- **Key stat**: "Disk-shaped craft 2.3x over-represented in psi reports"
- **Mobile**: Stats vertical scroll, Mack cards horizontal swipe.

### Section 11: "Missing Time and the Deep End"
- **Purpose**: Most extreme reports. Multi-category strangeness.
- **Visuals**: Co-occurrence heatmap. Abduction + missing time link. "Structured craft" as hub node diagram. Sample excerpts.
- **Data**: `high-strangeness.json` — co-occurrence matrix, multi-category reports.
- **Mobile**: Heatmap → simplified table, excerpts in expandable cards.

### Section 12: "The Communication"
- **Purpose**: What do they say? Communication content.
- **Visuals**: Horizontal stacked bar (content breakdown: personal 66%, spiritual 52%, etc.). Mack recurring themes. "84% do NOT want contact to stop."
- **Data**: `free-findings.json` — communication content stats.
- **Mobile**: Stacked bar vertical, themes as scroll list.

### Section 13: "The Convergence"
- **Purpose**: Cross-dataset validation. The thesis lands.
- **Visuals**: Overlap/matrix diagram (pattern × dataset). Evidence strength table. Convergence callouts.
- **Data**: `convergence.json` — cross-dataset pattern matrix with confirmation flags.
- **Key line**: "Five archives. Different decades. Different methods. Same phenomenon."
- **Mobile**: Matrix → stacked comparison cards.

### Section 14: "Field Notes"
- **Purpose**: Practical takeaway. The pocket reference.
- **Visuals**: Entity typology quick-reference (icon + name + trait + passability). Setting likelihood ranked list. Physical effect checklist. Consciousness indicators. Forward-looking trends.
- **Data**: Composited from all JSON bundles.
- **Mobile**: Designed as native-feeling card format — this section is optimized for phone use.

### Section 15: "Sources & Methodology"
- **Purpose**: Full transparency. Every stat sourced.
- **Visuals**: Dataset cards (source, count, range, methodology, limitations, link). Analysis methodology. Caveats. GitHub repo link.
- **Data**: Hardcoded metadata + links.
- **Key principle**: Every stat references its dataset and source (FREE article #, Rosales type code, NUFORC record count).
- **Mobile**: Dataset cards stack, methodology expandable.

## Reusable Components

### UI Components
- `ScrollReveal` — Framer Motion wrapper; fades/slides children into view on intersection
- `StatCounter` — Animated number counter (uses `useAnimatedCounter` hook)
- `SectionHeader` — Chapter number + title + subtitle, consistent typography
- `Card` — Dark glass-morphism card with hover/tap state
- `ExpandableCard` — Card with collapsible detail section (mobile-friendly)
- `ProgressBar` — Scroll progress indicator (fixed top)
- `SourceTag` — Inline citation badge ("NUFORC n=80,332" / "FREE Phase 2" / "Rosales Type G")

### Chart Components
- `AnimatedBar` — Recharts BarChart wrapped with Framer Motion entrance
- `AnimatedLine` — Recharts LineChart with animated path drawing
- `DonutChart` — Recharts PieChart configured as donut
- `HeatmapGrid` — Custom grid of colored cells (for co-occurrence, concentration)
- `StackedBar` — Recharts StackedBarChart with scroll trigger
- `SmallMultiples` — Grid of mini charts with shared axes

### Map Components
- `SightingHeatmap` — React-Leaflet with heatmap layer (NUFORC lat/lon)
- `EncounterMap` — Cluster markers for Rosales/Magonia locations
- `HotspotOverlay` — Toggleable density layers

## Visual Design

- **Theme**: Dark space aesthetic — near-black backgrounds (#0a0e1a), muted green accents (#7aaa88), grey tones matching the aliens
- **Typography**: Monospace for data/stats (JetBrains Mono or similar), clean sans-serif for body (system font stack for performance)
- **Color palette**:
  - Background: `#020408` → `#0a0e1a`
  - Primary accent: `#7aaa88` (the green from the banner)
  - Secondary: `#c8d8cc` (light grey-green)
  - Entity colors: Grey `#808080`, Nordic `#f5d442`, Reptilian `#22c55e`, Insectoid `#a855f7`, Robotic `#94a3b8`, Luminous `#06b6d4`, Human `#3b82f6`
  - Warning/alert: `#f59e0b`
  - Chart backgrounds: `#0f1420`
- **Animations**: Fade-up on scroll (200ms stagger for lists), number counters, chart bar/line growth, subtle float on entity icons
- **Grain**: Subtle CSS noise overlay matching banner texture

## Data JSON Bundle Specs

### nuforc-shapes.json
```ts
{
  topShapes: { shape: string; count: number }[];
  regionBreakdown: { region: string; shapes: Record<string, number> }[];
  distributionCurve: { logCount: number; frequency: number }[];
  totalRecords: number;
  topThreePercent: number;
}
```

### nuforc-geo.json
```ts
{
  points: { lat: number; lng: number; shape: string }[];  // downsampled
  concentrationRatios: { shape: string; region: string; ratio: number; pValue: number }[];
  stateShapeRates: { state: string; shape: string; rate: number }[];
}
```

### rosales-timeline.json
```ts
{
  typeCodes: { code: string; label: string; count: number; percent: number }[];
  byDecade: { decade: string; total: number; types: Record<string, number> }[];
  entityByDecade: { decade: string; types: Record<string, number> }[];  // percentages
}
```

### entity-taxonomy.json
```ts
{
  types: {
    name: string;
    category: string;  // "classic", "human-passing", "non-physical", etc.
    rosalesCount: number;
    magoniaCount: number;
    nuforcCount: number;
    passability: "HIGH" | "MEDIUM" | "LOW" | "NONE" | "N/A";
    description: string;
    tells: string[];
    sampleExcerpt: string;
  }[];
  humanPassing: {
    total: number;
    percent: number;
    behaviorComparison: { behavior: string; humanPassingPct: number; nonHumanPct: number }[];
    settingOverrepresentation: { setting: string; ratio: number }[];
  };
}
```

### high-strangeness.json
```ts
{
  categories: {
    name: string;
    theme: string;
    count: number;
    percent: number;
    avgCredibility: number;
    pnwRatio: number;
  }[];
  coOccurrence: { catA: string; catB: string; count: number }[];
  deepEnd: { state: string; shape: string; categories: string[]; excerpt: string }[];
  physicalEffects: { effect: string; count: number; percent: number }[];
}
```

### free-findings.json
```ts
{
  findings: { category: string; finding: string; value: string; unit: string }[];
  communicationContent: { type: string; percent: number }[];
  demographics: Record<string, string>;
  metadata: { phases: number; respondents: number; countries: number; questions: number };
}
```

### mack-cases.json
```ts
{
  cases: {
    id: string;
    pseudonym: string;
    gender: string;
    age: string;
    entityDescription: string;
    experienceTypes: string[];
    keyThemes: string[];
    transformativeEffects: string[];
  }[];
  demographics: { male: number; female: number; meanAge: number };
}
```

### convergence.json
```ts
{
  patterns: {
    pattern: string;
    datasets: string[];  // which datasets confirm
    strength: "strong" | "moderate" | "suggestive";
    evidence: string;
  }[];
}
```

### encounter-settings.json
```ts
{
  settings: { name: string; count: number; percent: number }[];
  humanPassingOverrep: { setting: string; ratio: number; count: number }[];
  timeOfDay: { hour: string; count: number }[];  // if parseable
}
```

## Deployment

- `next.config.ts`: `output: 'export'`, `basePath: '/ufolio'`, `images: { unoptimized: true }`
- GitHub Actions workflow: runs `build-site-data.py` → `next build` → deploys `out/` to `gh-pages` branch
- Custom domain optional (can add later via CNAME)

## Source Attribution

Every stat in the infographic includes a `SourceTag` component linking back to:
- Dataset name and record count
- For FREE data: specific article/chapter reference
- For Rosales: type code and entry count
- For NUFORC: field used and filter applied
- For Mack: chapter and pseudonym
- For Magonia: case ID range

## Out of Scope

- No user accounts or data submission
- No server-side rendering — purely static
- No real-time data updates — snapshot-in-time
- No 3D or WebGL — CSS/SVG/Canvas only for Safari compatibility
- No separate mobile app — responsive web only
