import { Component, NgZone, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SwUpdate } from '@angular/service-worker';
import { ApiType } from './entity/api.entity';
import { ApiService } from './service/api.service';
import { interval } from 'rxjs';
import { LookupEntity } from './entity/lookup.entity';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  loading: boolean = false;
  updating = false;
  lookup?: LookupEntity;
  error = false;


  constructor(
    private api: ApiService,
    private zone: NgZone,
    private swUpdate: SwUpdate,
    private snackBar: MatSnackBar
  ) {
    if (this.swUpdate.isEnabled) {
      this.swUpdate.available.subscribe((evt) => {
        this.updating = true;
        this.snackBar
          .open('Update is available', 'Update')
          .onAction()
          .subscribe(() =>
            this.swUpdate
              .activateUpdate()
              .then(() => document.location.reload())
          );
      });
      interval(10000).subscribe(() => {
        this.swUpdate.checkForUpdate();
      });
    }
    this.api.loading.subscribe(res => {
      console.log("api loading", res);
      this.zone.run(() => (this.loading = res));
    })

  }

  ngOnInit(): void {
    const params = new URLSearchParams(window.location.search);
    console.log(params);
    this.api.fetch(ApiType.LOOOKUP, {ip: params.get("ip")}).then((res) => {
      this.lookup = res as LookupEntity;
    }).catch((err) => {

    });
  }
  title = 'geo';
}
