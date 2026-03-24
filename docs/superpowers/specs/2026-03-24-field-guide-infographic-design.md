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

#### Entity Classification Methodology

The 32 entity types are classified from free-text descriptions using regex pattern matching — the same approach already proven in `entity_analysis.py`. Each type has a defined regex pattern (e.g., `\b(grey|gray)\s*(alien|being|entity)\b` for grey entities, `\b(nordic|blonde?|fair.?hair)\b` for nordics). The existing `entity_analysis.py` script already defines all 32 patterns and has been validated against the Rosales (8,666) and Magonia (923) corpora. The build script imports these patterns directly.

The `entityByDecade` field in `rosales-timeline.json` uses these regex-classified entity species counts (Grey, Nordic, Reptilian, etc.), NOT the structured encounter type codes (A-H). The encounter type codes are in the separate `byDecade` field.

#### Encounter Setting Classification

Settings (bedroom, roadside, rural, urban, military, water, mountain) are classified from free-text descriptions using the same regex approach defined in `entity_analysis.py` (see the `settings` dictionary). Each setting has a keyword pattern matched against the `description` column of Rosales and Magonia, and the `comments` column of NUFORC.

#### Geographic Data: No Geocoding Required

**Rosales and Magonia do NOT have lat/lon coordinates.** All geographic map visualizations use NUFORC data only (which has latitude/longitude). Rosales and Magonia geographic breakdowns use the existing `country` column (Magonia) and text-parsed country/region from the `location` column (Rosales) for bar charts and country-level aggregations — not point maps.

The `EncounterMap` component is scoped to NUFORC data. Rosales/Magonia geographic analysis uses `CountryBreakdown` bar charts instead.

#### NUFORC Heatmap Downsampling

The `nuforc-geo.json` file uses **0.25-degree hexbin aggregation** to reduce 65K+ raw points to ~2,000 hex cells with count values. This keeps the JSON under 200KB gzipped and renders smoothly on mobile Safari. The heatmap layer renders hex cells colored by density, not individual points.

#### Cross-Dataset Psi Correlation

Section 10's "disk-shaped craft 2.3x over-represented in psi reports" stat is computed by cross-tabulating NUFORC `shape` with the psi category flags from `high_strangeness_mining.py`. Added to `high-strangeness.json` as: `shapeCorrelations: { shape: string; category: string; ratio: number }[]`.

#### Data Size Budget

| Bundle | Target (gzipped) |
|--------|-------------------|
| `nuforc-geo.json` | < 200KB (hexbin aggregated) |
| `entity-taxonomy.json` | < 50KB |
| `nuforc-shapes.json` | < 20KB |
| `rosales-timeline.json` | < 30KB |
| `high-strangeness.json` | < 40KB |
| `free-findings.json` | < 10KB |
| `mack-cases.json` | < 15KB |
| `convergence.json` | < 10KB |
| `encounter-settings.json` | < 15KB |
| **Total** | **< 400KB gzipped** |

### Leaflet SSR Considerations

All map components must use `'use client'` and be loaded via `next/dynamic({ ssr: false })` to prevent SSR build failures from Leaflet's `window` dependency. All local asset references (custom markers, icons) must use a `basePath`-aware helper:

```ts
const assetPath = (path: string) => `${process.env.NEXT_PUBLIC_BASE_PATH || ''}${path}`;
```

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
- `SectionNav` — Sticky bottom bar (mobile) / sidebar dot nav (desktop) for jumping between 15 sections. Shows current section title. Collapse to hamburger when not in use.
- `ScrollableChart` — Container for horizontal-scroll charts on mobile with fade-edge affordances, `-webkit-overflow-scrolling: touch`, and optional scroll snap
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
- Custom domain optional (can add later via CNAME)

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [master]
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pandas numpy scipy
      - run: python scripts/build-site-data.py
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd site && npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site/out
```

## Source Attribution

Every stat in the infographic includes a `SourceTag` component linking back to:
- Dataset name and record count
- For FREE data: specific article/chapter reference (e.g., "FREE Article: Hernandez/Klimo/Schild UFO Report, Phase 2")
- For Rosales: type code and entry count
- For NUFORC: field used and filter applied
- For Mack: chapter and pseudonym
- For Magonia: case ID range

## Mobile-Specific Design Notes

### Section Navigation
`SectionNav` provides jump-to-section on all viewports. On mobile, it renders as a collapsible bottom bar showing current section title with a tap-to-expand chapter list. On desktop, it's a fixed dot-nav on the right edge.

### Horizontal Scroll Charts
Charts that are too wide for mobile (bar charts, timelines) render inside `ScrollableChart` containers with:
- `overflow-x: auto` and `-webkit-overflow-scrolling: touch`
- Fade gradients on left/right edges to signal scrollability
- Optional `scroll-snap-type: x mandatory` for discrete stops

### Heatmap Simplification
Co-occurrence heatmaps (Section 11) on viewports < 768px render as a **ranked list of top 10 co-occurring pairs** instead of the full matrix. Each pair shows the two categories + count in a compact card format.

### Touch Targets
All interactive elements (cards, toggles, map controls, nav items) have minimum 44×44px touch targets per Apple HIG.

## Phased Build Order

### Phase 1: Foundation + NUFORC Sections (Sections 1-3)
- Scaffold Next.js app, Tailwind dark theme, layout
- Build reusable UI components (ScrollReveal, StatCounter, SectionHeader, Card, ProgressBar, SectionNav)
- Build chart components (AnimatedBar, StackedBar)
- `build-site-data.py` — NUFORC aggregations only (shapes, geo hexbins)
- Sections 1 (opening), 2 (shapes), 3 (geography with Leaflet heatmap)
- Deploy to GitHub Pages — first visible milestone

### Phase 2: Rosales + Entity Taxonomy (Sections 4-7)
- `build-site-data.py` — add Rosales aggregations, entity classification (regex), timeline
- Build DonutChart, AnimatedLine, entity grid components
- Sections 4 (encounters), 5 (census), 6 (shift timeline), 7 (human-passing)
- This phase contains the heaviest data processing work

### Phase 3: Cross-Dataset + Consciousness (Sections 8-12)
- `build-site-data.py` — add encounter settings, high-strangeness, FREE findings, Mack cases, cross-dataset correlations
- Build HeatmapGrid, remaining chart variants
- Sections 8 (settings), 9 (body), 10 (mind), 11 (deep end), 12 (communication)

### Phase 4: Convergence + Polish (Sections 13-15)
- `build-site-data.py` — add convergence matrix
- Sections 13 (convergence), 14 (field notes), 15 (sources)
- Full responsive pass and mobile testing
- Performance audit (bundle sizes, Lighthouse)
- Final deploy

## Out of Scope

- No user accounts or data submission
- No server-side rendering — purely static
- No real-time data updates — snapshot-in-time
- No 3D or WebGL — CSS/SVG/Canvas only for Safari compatibility
- No separate mobile app — responsive web only
