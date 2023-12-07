import { Component, OnInit, HostListener, isDevMode } from "@angular/core";
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
import { MatSlideToggleChange } from "@angular/material/slide-toggle";
import { MatDialog } from '@angular/material/dialog';
import { GeoInputComponent } from "./components/geo-input/geo-input.component";
import { ActivatedRoute, EventType, Router } from "@angular/router";
import { MatButtonToggleChange } from "@angular/material/button-toggle";



@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {



  error = false;
  online = true;
  fullview = false;
  queryMode = QueryMode;
  isToggled = false;
  mode: QueryMode = QueryMode.IP;
  isAutoMode: boolean = true;
  modes: QueryMode[] = [QueryMode.GPS, QueryMode.IP];
  messages: string[] = [];
  icons: string[] = ['location_disabled', 'my_location'];
  $background = this.api.$background;
  $lookup = this.api.$lookup;
  $location = this.api.$location;
  page = this.activatedRoute.title;
  myIp?: string;

  private currentLookup?: LookupModel;
  private currentLocation?: LocationModel;

  constructor(
    private api: ApiService,
    private geoService: GeoLocationService,
    private swUpdate: SwUpdate,
    private ws: WebsocketService,
    private snackBar: MatSnackBar,
    public loader: LoaderService,
    public dialog: MatDialog,
    private router: Router,
    private activatedRoute: ActivatedRoute
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
          this.myIp = msg.content;
          this.router.routerState.snapshot.url == "/" &&
            this.router.navigate(['ip', this.myIp]);
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
    this.router.events.subscribe(res => {
      switch (res.type) {
        case EventType.ActivationEnd:
          this.mode = res.snapshot.component?.name == "LocationinfoComponent" ? QueryMode.GPS : QueryMode.IP;
          this.messages = [this.mode];
      }
    })
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
    switch (this.mode) {
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


  async onAutoMode($event: MatSlideToggleChange) {
    if ($event.checked) {
      switch (this.mode) {
        case this.queryMode.IP:
          return this.router.navigate(["ip", this.myIp]);
        case this.queryMode.GPS:
          return this.tryGeoLocation()
      }
    } else {
      this.openSearchDialog();
    }

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


  async onModeSwitch($event: MatButtonToggleChange) {
    switch ($event.value) {
      case this.queryMode.GPS:
        if (this.isAutoMode) {
          this.tryGeoLocation();
        } else if (this.currentLocation) {
          this.router.navigate(["location", this.currentLocation?.background]);
        } else {
          this.openSearchDialog();
        }
        break;
      case this.queryMode.IP:
        this.router.navigate(["ip", this.currentLookup?.ip || this.myIp]);
    }
  }

  openSearchDialog() {
    // this.searching = true;
    const dialogRef = this.dialog.open(GeoInputComponent, {
      panelClass: [
        'search-overlay-desktop',
        'is-active',
      ],
      // position: this.isMobile ? { top: '0' } : {},
      backdropClass: 'search-backdrop',
      delayFocusTrap: true,
      maxWidth: '800px',
      width: '80vw',
      data: this.mode,
    });
    dialogRef.afterClosed().subscribe((input) => {
      switch (this.mode) {
        case this.queryMode.IP:
          return this.router.navigate(["ip", input]);
        case this.queryMode.GPS:
          return this.router.navigate(["location", input]);
      }
    });
  }

  title = "geo";
}
