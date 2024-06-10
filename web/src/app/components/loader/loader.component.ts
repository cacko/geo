import { CommonModule } from '@angular/common';
import {  Component, ElementRef, OnInit, Renderer2 } from '@angular/core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { LoaderService } from '../../service/loader.service';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
})
export class LoaderComponent implements OnInit {

  constructor(
    private element: ElementRef,
    private renderer: Renderer2,
    private loader: LoaderService
  ) {

  }

  ngOnInit(): void {
    this.loader.$hidden.subscribe((hidden: boolean) => {
      hidden && this.renderer.setAttribute(this.element.nativeElement, "hidden", "1");
    });
    this.loader.$visible.subscribe((visible: boolean) => {
      visible && this.renderer.removeAttribute(this.element.nativeElement, "hidden");
    })
  }

}
