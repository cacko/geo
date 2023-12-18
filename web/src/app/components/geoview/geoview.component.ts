import { Component, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { Input, Output, HostBinding, EventEmitter } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity, BGMODE, LOOKUP_IMAGES } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';
import { View360Options, EquirectProjection } from "@egjs/ngx-view360";
import View360 from '@egjs/view360';
import { StorageService } from 'src/app/service/storage.service';
import { sample } from 'lodash-es';

@Component({
  selector: 'app-geoview',
  templateUrl: './geoview.component.html',
  styleUrl: './geoview.component.scss'
})
export class GeoviewComponent implements OnChanges {
  @ViewChild("viewer") public view360!: View360;

  private diffusionSrc = "";
  private rawSrc = ""

  options: Partial<View360Options> = {
    initialZoom: 0,
    projection: new EquirectProjection({
      src: LOOKUP_IMAGES.LOADING
    })
  }

  @Output() backgroundSrc: EventEmitter<string> = new EventEmitter<string>();
  @Output() backgroundStyle: EventEmitter<string> = new EventEmitter<string>();
  @Output() onRenewFinished: EventEmitter<void> = new EventEmitter<void>();
  @Input() mode?: BGMODE | null;
  @Input() locationbg?: string | null;

  onModeChange() {
    this.setModeBackground();
  }

  onLocationBGChange() {
    this.backgroundSrc.emit("");
    if (!this.locationbg) {
      return this.setBackground(LOOKUP_IMAGES.LOADING);
    }
    const fetchParams = {
      path: `${this.locationbg}`,
      style: ""
    }
    if (!this.diffusionSrc) {
      this.setBackground(LOOKUP_IMAGES.LOADING);
    } else if (this.storage.style) {
      fetchParams.style = sample(this.storage.style) as string;

    }
    this.isLoading = true;

    this.api.fetch(ApiType.BACKGROUND, fetchParams, false).then((res) => {
      const data = res as BackgroundEntity;
      let imgeUrl = data.url;
      this.diffusionSrc = imgeUrl;
      this.rawSrc = data.raw_url;
      this.backgroundStyle.emit(data.style);
      this.setModeBackground();
      this.isLoading = false;
    }).catch((err) => {
      this.isLoading = false;
    });
  }


  ngOnChanges(changes: SimpleChanges) {
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
    private storage: StorageService
  ) {
  }

  ngOnInit(): void {
    this.setBackground(LOOKUP_IMAGES.LOADING);
  }

  setModeBackground() {
    switch (this.mode) {
      case BGMODE.DIFFUSION:
        return this.setBackground(this.diffusionSrc);
      case BGMODE.RAW:
        return this.setBackground(this.rawSrc);
    }
  }

  setBackground(src: string) {
    this.view360.load(new EquirectProjection({ src }))
    this.backgroundSrc.emit(src);
  }

}
