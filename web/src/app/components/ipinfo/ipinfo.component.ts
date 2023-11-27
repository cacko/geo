import { Component, Input, OnInit } from '@angular/core';
import { LookupEntity } from 'src/app/entity/lookup.entity';
import { MatDialog } from '@angular/material/dialog';
import { MapComponent } from '../map/map.component';
import { MatSnackBar } from '@angular/material/snack-bar';
@Component({
  selector: 'app-ipinfo',
  templateUrl: './ipinfo.component.html',
  styleUrls: ['./ipinfo.component.scss']
})
export class IPInfoComponent implements OnInit {

  @Input() lookup!: LookupEntity
  img_url = "loading.png";
  gps !: string;

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {

  }

  ngOnInit(): void {
    if (!this.lookup) {
      return;
    }
    if (!this.lookup.location) {
      return;
    }
    this.gps = `${this.lookup.location[0]},${this.lookup.location[1]}`
  }

  onCopy($ev: boolean) {
    $ev && this.snackBar
      .open("GPS copied to clipboard", "Ok", { duration: 2000 })
  }

  onOpenMap($event: MouseEvent) {
    $event.preventDefault();
    const q = this.lookup.location?.slice(2).join(",");
    return window.open(`https://maps.google.com/?q=${q}`, "_blank",);
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
