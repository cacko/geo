import { Component, Input, OnInit } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity, LookupEntity } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';

@Component({
  selector: 'app-lookup-image',
  templateUrl: './lookup-image.component.html',
  styleUrls: ['./lookup-image.component.scss']
})
export class LookupImageComponent implements OnInit{

  constructor(
    private api: ApiService
  ) {

  }

  ngOnInit(): void {
    this.api.fetch(ApiType.BACKGROUND, {
      path: `${this.lookup.country} ${this.lookup.city}`,
      loader: "false"
    }, false).then((res) => {
      const data = res as BackgroundEntity;
      this.img_url = data.name;
      this.loaded = true;
    })
  }

  @Input() lookup !: LookupEntity

  loaded = false;
  img_url ?: string;


  getStyle(): { [key: string]: string } {
    return {
      'background': `url('https://geo.cacko.net/assets/b/${this.img_url}')`
    };
  }

}
