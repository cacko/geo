import { now } from "lodash-es";
import { LocationEntity } from "../entity/location.entity";

export class LocationModel implements LocationEntity {
    country!: string;
    country_iso!: string;
    city !: string;
    name !: string;
    subdivisions?: string;
    addressLine?: string;
    postCode?: string;
    location!: number[];
    timezone?: string;
    renew = false;
    ts?: string;

    backgroundSrc !: string;

    constructor(original: Object) {
        Object.assign(this, original);
        this.background = this.location.join(",");
    }

    get background(): string {
        return this.backgroundSrc;
    }

    set background(path: string) {
        this.backgroundSrc = path;
    }

    renewBackground(): boolean {
        const ts = now().toString();
        this.background = `${this.location.join(",")}/${ts}`;
        return true;
    }

}
