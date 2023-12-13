import { Component, OnInit, HostListener, isDevMode, NgZone } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { SwUpdate, VersionEvent } from "@angular/service-worker";
import { QueryMode } from "./entity/api.entity";
import { ApiService } from "./service/api.service";
import { interval } from "rxjs";
import { WebsocketService } from "./service/websocket.service";
import { WSCommand } from "./entity/websockets.entiity";
import { LookupModel } from "./models/lookup.model";
import { LoaderService } from "./service/loader.service";
import { GeoLocationService } from "./service/geo-location.service";
import { LocationModel } from "./models/location.model";
import { MatDialog } from '@angular/material/dialog';
import { GeoInputComponent } from "./components/geo-input/geo-input.component";
import { ActivatedRoute, EventType, Router } from "@angular/router";
import { StorageService } from "./service/storage.service";

import { saveAs } from 'file-saver';
import { Title } from "@angular/platform-browser";


@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {

  error = false;
  fullview = false;
  queryMode = QueryMode;
  modes: QueryMode[] = [QueryMode.GPS, QueryMode.IP];
  messages: string[] = [];
  icons: string[] = ['location_disabled', 'my_location'];
  download: string = "";
  $background = this.api.$background;
  $lookup = this.api.$lookup;
  $location = this.api.$location;
  $loading = this.loader.$visible;
  page = this.activatedRoute.title;

  private currentLookup?: LookupModel;
  private currentLocation?: LocationModel;

  constructor(
    public api: ApiService,
    private geoService: GeoLocationService,
    private swUpdate: SwUpdate,
    private ws: WebsocketService,
    private snackBar: MatSnackBar,
    public loader: LoaderService,
    public dialog: MatDialog,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public storage: StorageService,
    private titleService: Title
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
          storage.myip = msg.content;
          console.log("my ip is", storage.myip);
          if (this.router.routerState.snapshot.url == "/") {
            storage.mode = this.queryMode.IP;
            this.router.navigateByUrl(`ip/${this.storage.myip}`);
          } else {
            storage.mode = this.queryMode.MANUAL;
          }
      }
    });
    this.$location.subscribe(res => (this.currentLocation = res));
    this.$lookup.subscribe(res => (this.currentLookup = res));
  }

  sendMsg(source: string, content: string) {
    let message = {
      source,
      content,
    };

    this.ws.send(message);
  }

  ngOnInit(): void {
    this.loader.show();
  }


  @HostListener("window:keydown", ["$event"])
  hardRefresh(event: KeyboardEvent) {
    if (event.key === '/') {
      event.preventDefault();
      this.openSearchDialog();
    }
    if (event.shiftKey && event.metaKey && event.key === "r") {
      event.preventDefault();
      this.onRenew();
    }
  }


  onRenew() {
    this.loader.show();
    const mode = /\/ip\//.test(window.location.href) ? this.queryMode.IP : this.queryMode.GPS;
    switch (mode) {
      case this.queryMode.GPS:
        this.currentLocation &&
          this.currentLocation?.renewBackground() &&
          this.api.backgroundSubject.next(this.currentLocation?.background)
        break;

      case this.queryMode.IP:
        this.currentLookup &&
          this.currentLookup.renewBackground() &&
          this.api.backgroundSubject.next(this.currentLookup.background);
        break;
    }
  }
  onFullView() {
    this.fullview = !this.fullview;
  }

  downloadImage(src: string) {
    this.download = "";
    
    saveAs(src, `${this.titleService.getTitle()}.webp`);
    this.download = src;
  }

  onBackgroundSrc($event: string) {
    this.download = $event;
  }

  tryGeoLocation() {

    this.geoService.getCurrentPosition().subscribe({
      next: (res: GeolocationPosition) => {
        this.router.navigate(["location", `${res.coords.latitude},${res.coords.longitude}`]);
      }, error: (err: GeolocationPositionError) => {
        console.error(err);
        this.snackBar
          .open(err.message, "Ok", { duration: 2000, panelClass: 'warn' });
      }
    });
  }


  onModeSwitch($event: MouseEvent) {
    switch (this.storage.mode) {
      case this.queryMode.GPS:
        this.loader.show();
        return this.tryGeoLocation();
      case this.queryMode.IP:
        return this.router.navigate(["ip", this.storage.myip]);
      case this.queryMode.MANUAL:
        return this.openSearchDialog()
    }
  }

  openSearchDialog() {
    // this.searching = true;
    this.fullview = true;
    const dialogRef = this.dialog.open(GeoInputComponent, {
      panelClass: [
        'search-overlay',
        'is-active',
      ],
      // position: this.isMobile ? { top: '0' } : {},
      backdropClass: 'search-backdrop',
      delayFocusTrap: true,
      maxWidth: '100%',
      width: '100%',
    });
    dialogRef.afterClosed().subscribe((input) => {
      this.fullview = false;
      if (!input) {
        return;
      }
      if (LookupModel.isValidHostname(input)) {
        return this.router.navigate(["ip", input]);
      }
      return this.router.navigate(["location", input]);
    });
  }

  title = "geo";
}
