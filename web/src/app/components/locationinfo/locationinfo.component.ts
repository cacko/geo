import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MapComponent } from '../map/map.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LocationModel } from 'src/app/models/location.model';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/service/api.service';
import { LocationEntity } from 'src/app/entity/location.entity';
import { ApiType } from 'src/app/entity/api.entity';
import { Title } from '@angular/platform-browser';
@Component({
  selector: 'app-locationinfo',
  templateUrl: './locationinfo.component.html',
  styleUrls: ['./locationinfo.component.scss']
})
export class LocationinfoComponent implements OnInit {

  location?: LocationModel;
  img_url = "loading.png";
  gps?: string;
  title : string = "geo@location";

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private api: ApiService,
    private titleService: Title
  ) {

  }

  ngOnInit(): void {

    this.activatedRoute.params.subscribe(params => {
      const location = params["location"];
      if (LocationModel.isGPS(location)) {
        this.updateLocation(...LocationModel.parseGPS(location));
      } else {
        this.updateAddress(location);
      }
    });
  }

  private updateLocation(lat: number, lng: number) {
    this.api
      .fetch(ApiType.GPS, { path: `${lat}/${lng}` })
      .then((res) => {
        const model = new LocationModel(res as LocationEntity)
        this.location = model;
        this.api.locationSubject.next(this.location);
        this.api.backgroundSubject.next(model.background);
        this.gps = model.background
        this.titleService.setTitle(`${model.name}`);
      })
      .catch((err) => { });
  }


  private updateAddress(query: string) {
    this.api
      .fetch(ApiType.ADDRESS, { path: `${query}` })
      .then((res) => {
        const model = new LocationModel(res as LocationEntity);
        this.location = model;
        this.api.locationSubject.next(this.location);
        this.api.backgroundSubject.next(model.background);
        this.gps = model.background;
        this.titleService.setTitle(`${model.name}`);

      })
      .catch((err) => { });
  }


  onCopy($ev: boolean) {
    $ev && this.snackBar
      .open("GPS copied to clipboard", "Ok", { duration: 2000 })
  }

  onOpenMap($event: MouseEvent) {
    $event.preventDefault();
    const location = this.location as LocationModel;
    const query = location.location?.slice(0, 2).join(",");
    return window.open(`https://maps.google.com/?q=${query}`, "_blank",);
  }

  openMap(): void {
    if (!this.location) {
      return;
    }
    if (!this.location.location) {
      return;
    }
    const dialogRef = this.dialog.open(MapComponent,
      {
        data: {
          latitude: this.location.location[0],
          longitude: this.location.location[1]
        }
      });

    dialogRef.afterClosed().subscribe(result => {
      console.info(`Dialog result: ${result}`);
    });
  }

}
