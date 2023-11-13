import { now } from "lodash-es";
import { ISPEntity, LookupEntity } from "../entity/lookup.entity";

export class LookupModel implements LookupEntity {
  country?: string;
  country_iso?: string;
  city?: string;
  ip!: string;
  subdivisions?: string;
  location?: number[];
  timezone?: string;
  ISP?: ISPEntity;
  renew = false;

  ts ?: string;

  constructor(original: Object) {
    Object.assign(this, original);
  }

  get background(): string {
    const parts = [this.ip];
    if (this.ts) {
        parts.push(this.ts);
    }
    return parts.join("/")
  }

  renewBackground(): void {
    this.ts = now().toString();
  }

}
