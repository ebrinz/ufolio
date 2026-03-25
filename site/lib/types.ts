export interface Section {
  id: string;
  number: number;
  title: string;
  subtitle?: string;
}

export const SECTIONS: Section[] = [
  { id: "opening", number: 1, title: "The Signal in the Noise", subtitle: "102,385 reports. 5 datasets. 150 years." },
  { id: "shapes", number: 2, title: "The Scale of Sightings", subtitle: "What people see in the sky" },
  { id: "geography", number: 3, title: "The Geography of Lights", subtitle: "Where sightings cluster" },
  { id: "encounters", number: 4, title: "When It Gets Close", subtitle: "From sightings to encounters" },
  { id: "census", number: 5, title: "The Census of Visitors", subtitle: "Who shows up" },
  { id: "shift", number: 6, title: "The Shift", subtitle: "Entity types over time" },
  { id: "human-passing", number: 7, title: "The Ones Who Look Like Us", subtitle: "The 3.7% that could pass" },
  { id: "settings", number: 8, title: "Where They Show Up", subtitle: "Encounter settings" },
  { id: "body", number: 9, title: "What Happens to Your Body", subtitle: "Physical effects" },
  { id: "mind", number: 10, title: "What Happens to Your Mind", subtitle: "Consciousness and psi" },
  { id: "deep-end", number: 11, title: "Missing Time and the Deep End", subtitle: "The most extreme reports" },
  { id: "communication", number: 12, title: "The Communication", subtitle: "What they say" },
  { id: "convergence", number: 13, title: "The Convergence", subtitle: "When independent sources agree" },
  { id: "field-notes", number: 14, title: "Field Notes", subtitle: "The practical takeaway" },
  { id: "sources", number: 15, title: "Sources & Methodology", subtitle: "Full transparency" },
];

export interface ShapeData {
  shape: string;
  count: number;
}

export interface RegionBreakdown {
  region: string;
  shapes: Record<string, number>;
}

export interface NuforcShapes {
  topShapes: ShapeData[];
  regionBreakdown: RegionBreakdown[];
  distributionCurve: { logCount: number; frequency: number }[];
  shapesCumulative?: { shape: string; count: number; pct: number; cumulativePct: number }[];
  pct80Threshold?: string;
  totalRecords: number;
  topThreePercent: number;
  uniqueShapes?: number;
}

export interface HexCell {
  lat: number;
  lng: number;
  count: number;
}

export interface ConcentrationRatio {
  shape: string;
  region: string;
  ratio: number;
  pValue: number;
  significant: boolean;
}

export interface NuforcGeo {
  hexCells: HexCell[];
  concentrationRatios: ConcentrationRatio[];
  topInsight: string;
}
