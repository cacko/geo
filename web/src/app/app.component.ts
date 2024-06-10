import { Component, OnInit, HostListener, isDevMode } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { SwUpdate, VersionEvent } from "@angular/service-worker";
import { QueryMode } from "./entity/api.entity";
import { ApiService } from "./service/api.service";
import { BehaviorSubject, interval, filter } from "rxjs";
import { WebsocketService } from "./service/websocket.service";
import { WSCommand } from "./entity/websockets.entiity";
import { LookupModel } from "./models/lookup.model";
import { LoaderService } from "./service/loader.service";
import { GeoLocationService } from "./service/geo-location.service";
import { LocationModel } from "./models/location.model";
import { MatDialog } from '@angular/material/dialog';
import { GeoInputComponent } from "./components/geo-input/geo-input.component";
import { ActivatedRoute, NavigationStart, Router } from "@angular/router";
import { StorageService } from "./service/storage.service";

import { saveAs } from 'file-saver';
import { Title } from "@angular/platform-browser";
import { BGMODE, BGMODEICONS } from "./entity/lookup.entity";
import { Platform } from "@angular/cdk/platform";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {

  error = false;
  fullview = false;
  queryMode = QueryMode;
  BG_MODE_ICONS = BGMODEICONS;
  BG_MODES = BGMODE;
  bgModes = [BGMODE.RAW, BGMODE.DIFFUSION];
  modes: QueryMode[] = [QueryMode.GPS, QueryMode.IP];
  messages: string[] = [];
  icons: string[] = ['location_disabled', 'my_location'];
  $background = this.api.$background;
  $lookup = this.api.$lookup;
  $location = this.api.$location;
  page = this.activatedRoute.title;
  diffusionStyle: string = "";

  metaKeyName = this.platform.IOS

  private currentLookup?: LookupModel;
  private currentLocation?: LocationModel;

  downloadSubject = new BehaviorSubject<string>("");
  $download = this.downloadSubject.asObservable();

  bgModeSubject = new BehaviorSubject<BGMODE>(BGMODE.DIFFUSION);
  $bgMode = this.bgModeSubject.asObservable();

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
    private titleService: Title,
    private platform: Platform
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

    router.events
      .pipe(
        filter(
          (event: any) =>
            (event instanceof NavigationStart)

        )
      )
      .subscribe({
        next: (event: NavigationStart) => {
          console.group("NavigationStart Event");
          if (event.restoredState) {
            console.warn(
              "restoring navigation id:",
              event.restoredState.navigationId
            );

          }
          console.groupEnd();
        }, error: () => {

        }

      }
      )
      ;

    this.ws.messages.subscribe((msg) => {
      switch (msg.command) {
        case WSCommand.IP:
          storage.myip = msg.content.shift() || "";
          if (this.router.routerState.snapshot.url == "/") {
            storage.mode = this.queryMode.IP;
            this.router.navigateByUrl(`ip/${this.storage.myip}`);
          } else {
            storage.mode = this.queryMode.MANUAL;
          }
          break;
        case WSCommand.STYLES:
          this.storage.styles = msg.content;
          break;
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



  onBackgroundStyle($event: string) {
    this.diffusionStyle = $event;
  }

  @HostListener("window:keydown", ["$event"])
  hardRefresh(event: KeyboardEvent) {
    if (event.key === '/') {
      event.preventDefault();
      this.openSearchDialog();
    }
    if (event.shiftKey && event.metaKey) {

      switch (event.key) {
        case "r":
          event.preventDefault();
          return this.onRenew();
        case "f":
          event.preventDefault();
          return this.onFullView();
        case "v":
          event.preventDefault();
          return this.onBgMode();
      }
    }
  }


  onRenew() {
    this.loader.show();
    const mode = /\/ip\//.test(window.location.href) ? this.queryMode.IP : this.queryMode.GPS;
    this.bgModeSubject.next(BGMODE.DIFFUSION);
    this.bgModes = [BGMODE.RAW, BGMODE.DIFFUSION];
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

  onBgMode() {
    const next = this.bgModes.shift() || BGMODE.DIFFUSION;
    this.bgModes.push(next);
    this.bgModeSubject.next(next);
  }

  downloadImage(src: string) {
    saveAs(src, `${this.titleService.getTitle()}.webp`);
  }

  // onBackgroundSrc($event: string) {
  //   this.download = $event;
  // }

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


  onStyleChange($event: any) {
    this.storage.style = $event as string;
    this.onRenew();
  }

  title = "geo";
}
