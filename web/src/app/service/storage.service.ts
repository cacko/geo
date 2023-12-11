import { Injectable } from '@angular/core';
import { QueryMode } from '../entity/api.entity';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  private _myIp = "";
  private _mode: QueryMode = QueryMode.IP;
  constructor(

  ) { }

  set myip(value: string) {
    this._myIp = value;
  }

  get myip() {
    return this._myIp
  }

  set mode(value: QueryMode) {
    this._mode = value;
  }

  get mode() {
    return this._mode;
  }

}
