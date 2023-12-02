import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MapComponent } from '../map/map.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LocationModel } from 'src/app/models/location.model';
@Component({
  selector: 'app-locationinfo',
  templateUrl: './locationinfo.component.html',
  styleUrls: ['./locationinfo.component.scss']
})
export class LocationinfoComponent implements OnInit {

  @Input() location!: LocationModel;
  img_url = "loading.png";
  gps !: string;

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {

  }

  ngOnInit(): void {
    if (!this.location) {
      return;
    }
    if (!this.location.location) {
      return;
    }
    this.gps = `${this.location.location[0]},${this.location.location[1]}`
  }

  onCopy($ev: boolean) {
    $ev && this.snackBar
      .open("GPS copied to clipboard", "Ok", { duration: 2000 })
  }

  onOpenMap($event: MouseEvent) {
    $event.preventDefault();
    const query = this.location.location?.slice(0, 2).join(",");
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
