export interface ISPEntity {
  name: string;
  id: number;
}

export enum LOOKUP_IMAGES {
  LOADING="https://cdn.cacko.net/geo/loading.webp"
}

export interface LookupEntity {
  country?: string
  country_iso?: string
  city?: string
  ip: string;
  subdivisions?: string;
  location?: number[];
  timezone?: string;
  ISP?: ISPEntity;
}

export interface BackgroundEntity {
  name: string;
  url: string;
  raw_url: string;
  style: string;
}

export enum BGMODE {
  DIFFUSION = "diffusion",
  RAW = "raw"
}

export enum BGMODEICONS {
  diffusion = "cruelty_free",
  raw = "vrpano"
}