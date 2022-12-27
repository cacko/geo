import { Component, Input, OnInit } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity, LookupEntity } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';

@Component({
  selector: 'app-ipinfo',
  templateUrl: './ipinfo.component.html',
  styleUrls: ['./ipinfo.component.scss']
})
export class IPInfoComponent implements OnInit {

  @Input() lookup!: LookupEntity;
  img_url = "loading.png";
  loaded = false

  constructor(
    private api: ApiService
  ) {

  }

  ngOnInit(): void {
    this.loaded = false;
    setTimeout(() => {
      this.api.fetch(ApiType.BACKGROUND, {
        path: `${this.lookup.country} ${this.lookup.city}`,
        loader: "false"
      }, false).then((res) => {
        const data = res as BackgroundEntity;
        this.img_url = data.name;
        this.loaded = true;
      }).catch((err) => {

      });
    }, 0);

  }

}
