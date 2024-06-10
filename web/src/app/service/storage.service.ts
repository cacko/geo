import { Injectable } from '@angular/core';
import { QueryMode } from '../entity/api.entity';
import { kebabCase } from 'lodash-es';
import { BehaviorSubject, sample } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  readonly KEY_MYIP = "myip";
  readonly KEY_MODE = "mode";
  readonly KEY_STYLES = "styles";
  readonly KEY_STYLE = "style";

  private styleSubject = new BehaviorSubject<string>(this.style);
  $style = this.styleSubject.asObservable();

  private backgroundSrc ?: string


  constructor(

  ) { }

  private store(value: any, key: string) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  private fetch(key: string, def: any = null): any {
    const data = localStorage.getItem(key);
    return data !== null ? JSON.parse(data) : def;
  }

  set myip(value: string) {
    this.store(value, this.KEY_MYIP);
  }

  get myip(): string {
    return this.fetch(this.KEY_MYIP, "");
  }

  set mode(value: QueryMode) {
    this.store(value, this.KEY_MODE);
  }

  get mode(): QueryMode {
    return this.fetch(this.KEY_MODE, QueryMode.IP);
  }

  set styles(value: string[]) {
    localStorage.setItem(this.KEY_STYLES, JSON.stringify(value));
  }

  get styles(): string[] {
    return this.fetch(this.KEY_STYLES, []);
  }

  set style(value: string) {
    this.store(value, this.KEY_STYLE);
    this.styleSubject.next(value);
  }

  get style(): string {
    return this.fetch(this.KEY_STYLE, sample(this.styles));
  }


}
