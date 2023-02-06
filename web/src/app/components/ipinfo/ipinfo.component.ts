import { Component, Input, OnInit } from '@angular/core';
import { ApiType } from 'src/app/entity/api.entity';
import { BackgroundEntity, LookupEntity } from 'src/app/entity/lookup.entity';
import { ApiService } from 'src/app/service/api.service';
import { MatDialog } from '@angular/material/dialog';
import { MapComponent } from '../map/map.component';
@Component({
  selector: 'app-ipinfo',
  templateUrl: './ipinfo.component.html',
  styleUrls: ['./ipinfo.component.scss']
})
export class IPInfoComponent implements OnInit {

  @Input() lookup!: LookupEntity 
  img_url = "loading.png";
  loaded = false

  constructor(
    private api: ApiService,
    private dialog: MatDialog
  ) {

  }

  ngOnInit(): void {
    // this.loaded = false;
    // setTimeout(() => {
    //   this.api.fetch(ApiType.BACKGROUND, {
    //     path: `${this.lookup.ip}`,
    //     loader: "false"
    //   }, false).then((res) => {
    //     const data = res as BackgroundEntity;
    //     this.img_url = data.name;
    //     this.loaded = true;
    //   }).catch((err) => {

    //   });
    // }, 0);

  }

  openMap(): void {
    if (!this.lookup) {
      return;
    }
    if (!this.lookup.location) {
      return;
    }
    const dialogRef = this.dialog.open(MapComponent,
      {
        data: {
          latitude: this.lookup.location[0],
          longitude: this.lookup.location[1]
        }
      });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

}
