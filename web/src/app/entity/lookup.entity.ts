export interface ISPEntity {
  name: string;
  id: number;
}

export interface LookupEntity {
  country?: string
  country_iso ?: string
  city?: string
  ip: string;
  subdivisions?: string;
  location?: number[];
  timezone ?: string;
  ISP ?: ISPEntity;
}