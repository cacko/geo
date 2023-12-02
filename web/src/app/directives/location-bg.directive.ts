import { Directive, ElementRef, Input, OnInit, HostListener, HostBinding } from '@angular/core';
import { ApiType } from '../entity/api.entity';
import { BackgroundEntity, LookupEntity } from '../entity/lookup.entity';
import { ApiService } from '../service/api.service';
import { now } from 'lodash-es';

@Directive({
  selector: '[locationbg]'
})
export class LocationBgDirective implements OnInit {

  @Input() locationbg?: string | null;
  @HostBinding('class.loading') isLoading = false;
  constructor(
    private api: ApiService,
    private el: ElementRef,
  ) {
  }

  @HostListener('change') ngOnChanges() {
    console.log("changes",this.locationbg);
    this.isLoading = true;
    if (!this.locationbg) {
      return this.setBackground("/bg/loading.webp");
    }
    const fetchParams = {
      path: `${this.locationbg}`,
    }
    this.api.fetch(ApiType.BACKGROUND, fetchParams, false).then((res) => {
      const data = res as BackgroundEntity;
      let imgeUrl = data.url;
      this.setBackground(imgeUrl);
      this.isLoading = false;

    }).catch((err) => {

    });
  }

  ngOnInit(): void {
    this.setBackground("/bg/loading.webp");
  }

  protected setBackground(img: string) {
    this.el.nativeElement.style.backgroundImage = `url('https://geo.cacko.net${img}')`;
    // this.el.nativeElement.cl
  }

}
