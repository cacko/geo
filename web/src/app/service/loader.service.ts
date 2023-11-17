import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  private visibleSubject = new Subject<boolean>();
  visible = this.visibleSubject.asObservable();

  constructor() { }

  show() {
    this.visibleSubject.next(true);
  }

  hide() {
    this.visibleSubject.next(false);
  }

}
