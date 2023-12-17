import { Component } from '@angular/core';
import { ElementRef, Input, Output,HostListener, HostBinding, EventEmitter } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';
import { View360Options, EquirectProjection } from "@egjs/ngx-view360";

@Component({
  selector: 'app-geoview',
  templateUrl: './geoview.component.html',
  styleUrl: './geoview.component.scss'
})
export class GeoviewComponent {

  options: Partial<View360Options> = {
    fov: 120,
    projection: new EquirectProjection({
      src: "/bg/loading.webp",
    })
  }

  @Output() backgroundSrc: EventEmitter<string> = new EventEmitter<string>();
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
    const src = `https://geo.cacko.net${img}`;

    this.options = {
      ...this.options,
      projection: new EquirectProjection({
        src: src
      })
    };
    this.backgroundSrc.emit(src);
  }

}
