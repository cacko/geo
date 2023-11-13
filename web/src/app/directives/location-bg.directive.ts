import { Directive, ElementRef, Input, OnInit, HostListener, HostBinding } from '@angular/core';
import { ApiType } from '../entity/api.entity';
import { BackgroundEntity, LookupEntity } from '../entity/lookup.entity';
import { ApiService } from '../service/api.service';

@Directive({
  selector: '[locationbg]'
})
export class LocationBgDirective implements OnInit {

  @Input() locationbg?: string;
  @HostBinding('class.loading') isLoading = false;
  constructor(
    private api: ApiService,
    private el: ElementRef,
  ) {
  }

  @HostListener('change') ngOnChanges() {
    console.log("changes",this.locationbg);
    if (!this.locationbg) {
      this.setBackground("/bg/loading.png");
    }
    this.isLoading = true;
    this.api.fetch(ApiType.BACKGROUND, {
      path: `${this.locationbg}`,
      loader: "false"
    }, false).then((res) => {
      const data = res as BackgroundEntity;
      this.setBackground(data.url);
      this.isLoading = false;
    }).catch((err) => {

    });
  }

  ngOnInit(): void {
    this.setBackground("/bg/loading.png");
  }

  protected setBackground(img: string) {
    this.el.nativeElement.style.backgroundImage = `url('https://geo.cacko.net${img}')`;
    // this.el.nativeElement.cl
  }

}
