import { Directive, ElementRef, Input, Output, OnInit, HostListener, HostBinding, EventEmitter } from '@angular/core';
import { ApiType } from '../entity/api.entity';
import { BackgroundEntity, LookupEntity } from '../entity/lookup.entity';
import { ApiService } from '../service/api.service';
import { now } from 'lodash-es';

@Directive({
  selector: '[locationbg]'
})
export class LocationBgDirective implements OnInit {

  @Output() backgroundSrc: EventEmitter<string> = new EventEmitter<string>()
  @Input() locationbg?: string | null;
  @HostBinding('class.loading') isLoading = false;
  constructor(
    private api: ApiService,
    private el: ElementRef,
  ) {
  }

  @HostListener('change') ngOnChanges() {
    this.backgroundSrc.emit("");
    if (!this.locationbg) {
      return this.setBackground("/bg/loading.webp");
    }
    this.isLoading = true;
    const fetchParams = {
      path: `${this.locationbg}`,
    }
    this.api.fetch(ApiType.BACKGROUND, fetchParams, false).then((res) => {
      const data = res as BackgroundEntity;
      let imgeUrl = data.url;
      this.setBackground(imgeUrl);
      this.isLoading = false;

    }).catch((err) => {
      this.isLoading = false;
    });
  }

  ngOnInit(): void {
    this.setBackground("/bg/loading.webp");
  }

  protected setBackground(img: string) {
    const src = `https://geo.cacko.net${img}`
    this.el.nativeElement.style.backgroundImage = `url('${src}')`;
    this.backgroundSrc.emit(src);
  }

}
