export interface Cafe {
  name: string;
  address: string;
  x: number;
  y: number;
  distance?: number;
  place_url?: string;
  phone?: string;
  category_name?: string;
}

export interface BlogAnalysis {
  workScore: number;
  outletLevel: string;
  noiseLevel: string;
  spaceLevel: string;
  tableHeight: string;
  timeLimit: string;
  hasWifi: boolean;
  hasParking: boolean;
  totalScore: number;
  signalColor: string;
  blogCount: number;
  blogUrls: string[];
  blogItems: BlogItem[];
  description: string;
  keywords: {[key: string]: number};
  themes: string[];
}

export interface BlogItem {
  url: string;
  title: string;
  description: string;
}

export interface UserLocation {
  latitude: number;
  longitude: number;
}
