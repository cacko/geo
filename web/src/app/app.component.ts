import { Component, OnInit, HostListener, isDevMode } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { SwUpdate, VersionEvent } from "@angular/service-worker";
import { ApiType } from "./entity/api.entity";
import { ApiService } from "./service/api.service";
import { Subject, combineLatest, interval, last, lastValueFrom, shareReplay, withLatestFrom } from "rxjs";
import { LookupEntity } from "./entity/lookup.entity";
import { WebsocketService } from "./service/websocket.service";
import { WSCommand } from "./entity/websockets.entiity";
import { LookupModel } from "./models/lookup.model";
import { LoaderService } from "./service/loader.service";
import { GeoLocationService } from "./service/geo-location.service";
import { LocationModel } from "./models/location.model";
import { LocationEntity } from "./entity/location.entity";

export enum ApiMode {
  IP = "ip",
  GPS = "gps"
}

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {
  private lookupSubject = new Subject<LookupModel>();
  $lookup = this.lookupSubject.asObservable();
  private locationSubject = new Subject<LocationModel>();
  $location = this.locationSubject.asObservable();
  private backgroundSubject = new Subject<string>();
  $background = this.backgroundSubject.asObservable();

  error = false;
  online = true;
  fullview = false;
  modes = ApiMode;
  mode = ApiMode.IP;
  messages: string[] = [];

  private currentLookup?: LookupModel;
  private currentLocation?: LocationModel;

  constructor(
    private api: ApiService,
    private geoService: GeoLocationService,
    private swUpdate: SwUpdate,
    private ws: WebsocketService,
    private snackBar: MatSnackBar,
    public loader: LoaderService
  ) {
    if (!isDevMode()) {
      this.swUpdate.versionUpdates.subscribe((evt: VersionEvent) => {
        if (evt.type == "VERSION_READY") {
          this.snackBar
            .open("Update is available", "Update", { duration: 15000 })
            .afterDismissed()
            .subscribe(() =>
              this.swUpdate
                .activateUpdate()
                .then(() => document.location.reload())
            );
        }
      });
      interval(10000).subscribe(() => {
        this.swUpdate.checkForUpdate();
      });
    }

    this.ws.messages.subscribe((msg) => {
      switch (msg.command) {
        case WSCommand.IP:
          this.updateGeoIP(msg.content);
      }
      if (msg.command === WSCommand.IP) {
        this.messages.push(msg.content);
      }
    });
  }

  sendMsg(source: string, content: string) {
    let message = {
      source,
      content,
    };

    this.ws.send(message);
  }

  ngOnInit(): void {
    const params = new URLSearchParams(window.location.search);
    const ip = params.get("ip");
    ip && this.updateGeoIP(ip);
  }

  @HostListener("window:keydown", ["$event"])
  hardRefresh(event: KeyboardEvent) {
    if (event.shiftKey && event.metaKey && event.key === "r") {
      event.preventDefault();
      this.onRenew();
    }
  }

  onRenew() {
    this.loader.show();
    switch (this.mode) {
      case this.modes.GPS:
        this.currentLocation &&
          this.currentLocation?.renewBackground() &&
          this.backgroundSubject.next(this.currentLocation?.background)
        break;

      case this.modes.IP:
        this.currentLookup &&
          this.currentLookup.renewBackground() &&
          this.backgroundSubject.next(this.currentLookup.background);
        break;
    }
  }

  onFullView() {
    this.fullview = !this.fullview;
  }

  private updateLocation(res: GeolocationPosition) {
    this.api
      .fetch(ApiType.GPS, { path: `${res.coords.latitude}/${res.coords.longitude}` })
      .then((res) => {
        const model = new LocationModel(res as LocationEntity)
        this.locationSubject.next(model);
        this.backgroundSubject.next(model.background);
        this.currentLocation = model;
      })
      .catch((err) => { });
  }


  private updateGeoIP(ip: string | null) {
    this.api
      .fetch(ApiType.LOOKUP, { path: ip })
      .then((res) => {
        const model = new LookupModel(res as LookupEntity)
        this.lookupSubject.next(model);
        this.backgroundSubject.next(model.background);
        this.currentLookup = model;
      })
      .catch((err) => { });
  }


  async onLocation($event: MouseEvent) {
    this.mode = this.mode === this.modes.IP ? this.modes.GPS : this.modes.IP;
    switch (this.mode) {
      case this.modes.GPS:
        this.geoService.getCurrentPosition().subscribe({
          next: (res: GeolocationPosition) => {
            console.debug(res);
            this.updateLocation(res);
            this.messages = ["My Location"];
          }, error: (err: GeolocationPositionError) => {
            console.error(err);
            this.snackBar
              .open(err.message, "Ok", { duration: 2000, panelClass: 'warn' });
          }
        });
        break;
      case this.modes.IP:
        this.currentLookup && this.backgroundSubject.next(this.currentLookup.background);
        this.currentLookup && (this.messages = [this.currentLookup.ip]);
    }
  }

  title = "geo";
}
