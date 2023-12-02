export interface LocationEntity {
    country: string;
    country_iso: string;
    city: string;
    name: string;
    subdivisions?: string;
    location?: number[];
    addressLine?: string;
    postCode?: string;

}