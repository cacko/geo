import { Injectable } from '@angular/core';
import { QueryMode } from '../entity/api.entity';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  readonly KEY_MYIP = "myip";
  readonly KEY_MODE = "mode";


  constructor(

  ) { }

  private store(value: any, key: string) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  private fetch(key: string, def: any = null): any {
    const data = localStorage.getItem(key);
    console.log(data);
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

}
