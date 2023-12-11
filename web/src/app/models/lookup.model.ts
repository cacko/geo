import { now } from "lodash-es";
import { ISPEntity, LookupEntity } from "../entity/lookup.entity";
import ipRegex from "ip-regex";

function isValidHostname(value: any) {
  if (typeof value !== 'string') return false

  const validHostnameChars = /^[a-zA-Z0-9-.]{1,253}\.?$/g
  if (!validHostnameChars.test(value)) {
    return false
  }

  if (value.endsWith('.')) {
    value = value.slice(0, value.length - 1)
  }

  if (value.length > 253) {
    return false
  }

  const labels = value.split('.')

  const isValid = labels.every(function (label: string) {
    const validLabelChars = /^([a-zA-Z0-9-]+)$/g

    const validLabel = (
      validLabelChars.test(label) &&
      label.length < 64 &&
      !label.startsWith('-') &&
      !label.endsWith('-')
    )

    return validLabel
  })

  return isValid
}


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

  static isIPv4(query: string): boolean {
    return ipRegex.v4().test(query);
  }

  static isValidHostname(query: string): boolean {
    return isValidHostname(query);
  }

  renewBackground(): boolean {
    const ts = now().toString();
    this.background = `${this.ip}/${ts}`;
    return true;
  }

}
