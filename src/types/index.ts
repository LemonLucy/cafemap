export interface Cafe {
  name: string;
  address: string;
  x: number;
  y: number;
  distance?: number;
}

export interface BlogAnalysis {
  workScore: number;
  outletLevel: string;
  noiseLevel: string;
  spaceLevel: string;
  hasWifi: boolean;
  totalScore: number;
  signalColor: string;
  blogCount: number;
  blogUrls: string[];
  description: string;
}
