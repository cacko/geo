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
  ts?: string;

  backgroundSrc !: string;

  constructor(original: Object) {
    Object.assign(this, original);
    this.background = this.ip;
  }

  get background(): string {
    return this.backgroundSrc;
  }

  set background(path: string) {
    this.backgroundSrc = path;
  }

  renewBackground(): boolean {
    const ts = now().toString();
    this.background = `${this.ip}/${ts}`;
    return true;
  }

}
