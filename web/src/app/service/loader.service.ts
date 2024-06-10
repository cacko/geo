import { ElementRef, Injectable, Renderer2 } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  private visibleSubject = new BehaviorSubject<boolean>(true);
  $visible = this.visibleSubject.asObservable();
  private hiddenSubject = new BehaviorSubject<boolean>(false);
  $hidden = this.hiddenSubject.asObservable();

  constructor(

  ) { }

  show() {
    this.visibleSubject.next(true);
    this.hiddenSubject.next(false)
  }

  hide() {
    this.visibleSubject.next(false);
    this.hiddenSubject.next(true);
  }

}
