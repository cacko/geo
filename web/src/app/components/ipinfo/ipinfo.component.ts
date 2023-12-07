import { Component, Input, OnInit } from '@angular/core';
import { LookupEntity } from 'src/app/entity/lookup.entity';
import { MatDialog } from '@angular/material/dialog';
import { MapComponent } from '../map/map.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LookupModel } from 'src/app/models/lookup.model';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/service/api.service';
import { ApiType } from 'src/app/entity/api.entity';
@Component({
  selector: 'app-ipinfo',
  templateUrl: './ipinfo.component.html',
  styleUrls: ['./ipinfo.component.scss']
})
export class IPInfoComponent implements OnInit {

  lookup ?: LookupModel;
  img_url = "loading.png";
  gps ?: string;
  title = "ip";

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private acitivatedRoute: ActivatedRoute,
    private api: ApiService
  ) {

  }

  ngOnInit(): void {

    this.acitivatedRoute.params.subscribe(params => {
      this.updateGeoIP(params["ip"]);
    });


  }

  private updateGeoIP(ip: string | null) {
    this.api
      .fetch(ApiType.LOOKUP, { path: ip })
      .then((res) => {
        const model = new LookupModel(res as LookupEntity)
        this.lookup = model as LookupModel;
        const location = this.lookup.location as number[];
        this.gps = `${location[0]},${location[1]}`;
        this.api.backgroundSubject.next(model.background);
        this.api.lookupSubject.next(this.lookup);
      })
      .catch((err) => { });
  }

  onCopy($ev: boolean) {
    $ev && this.snackBar
      .open("GPS copied to clipboard", "Ok", { duration: 2000 })
  }

  onOpenMap($event: MouseEvent) {
    $event.preventDefault();
    const lookup = this.lookup as LookupModel;
    const query = lookup.location?.slice(0, 2).join(",");
    return window.open(`https://maps.google.com/?q=${query}`, "_blank",);
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
      console.info(`Dialog result: ${result}`);
    });
  }

}
