import { Component, OnChanges, SimpleChange, SimpleChanges } from '@angular/core';
import { ElementRef, Input, Output, HostListener, HostBinding, EventEmitter } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity, BGMODE } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';
import { View360Options, EquirectProjection } from "@egjs/ngx-view360";

@Component({
  selector: 'app-geoview',
  templateUrl: './geoview.component.html',
  styleUrl: './geoview.component.scss'
})
export class GeoviewComponent implements OnChanges {


  private diffusionSrc = "";
  private rawSrc = ""

  options: Partial<View360Options> = {
    projection: new EquirectProjection({
      src: "/bg/loading.webp",
    })
  }

  @Output() backgroundSrc: EventEmitter<string> = new EventEmitter<string>();

  @Input() mode?: BGMODE | null;

  @Input() locationbg?: string | null;

  onModeChange() {
    console.log(`mnde ${this.mode}`);
    this.setModeBackground();
  }

  onLocationBGChange() {
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
      this.diffusionSrc = `https://geo.cacko.net${imgeUrl}`;
      this.rawSrc = data.raw_url;
      this.setModeBackground();
      this.isLoading = false;

    }).catch((err) => {
      this.isLoading = false;
    });
  }


  ngOnChanges(changes: SimpleChanges) {
    console.log(`locationbg ${this.locationbg}`);
    console.log(changes);
    Object.keys(changes).forEach(changed => {
      switch (changed) {
        case "mode":
          return this.onModeChange();
        case "locationbg":
          return this.onLocationBGChange();
      }
    })
  }


  @HostBinding('class.loading') isLoading = false;
  constructor(
    private api: ApiService,
    private el: ElementRef,
  ) {
  }

  ngOnInit(): void {
    this.setBackground("/bg/loading.webp");
  }

  protected setModeBackground() {
    switch (this.mode) {
      case BGMODE.DIFFUSION:
        return this.setBackground(this.diffusionSrc);
      case BGMODE.RAW:
        return this.setBackground(this.rawSrc);
    }
  }

  protected setBackground(src: string) {
    this.options = {
      ...this.options,
      projection: new EquirectProjection({
        src: src
      })
    };
    this.backgroundSrc.emit(src);
  }

}
