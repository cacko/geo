import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DomSanitizer } from '@angular/platform-browser';

export interface DialogData {
  latitude: number;
  longitude: number;
}

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent {

  location: string = "";
  url: string = ""

  constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData, public sanitizer: DomSanitizer
  ) {
    this.location = [data.latitude, data.longitude].join(",");
    this.url = `https://maps.google.com/?q=${this.location}`
    console.log(this.location);
    console.log(this.url);
  }
}
