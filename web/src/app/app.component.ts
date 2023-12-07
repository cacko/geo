import { Component, OnInit, HostListener, isDevMode } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { SwUpdate, VersionEvent } from "@angular/service-worker";
import { ApiType } from "./entity/api.entity";
import { ApiService } from "./service/api.service";
import { Subject, interval } from "rxjs";
import { LookupEntity } from "./entity/lookup.entity";
import { WebsocketService } from "./service/websocket.service";
import { WSCommand } from "./entity/websockets.entiity";
import { LookupModel } from "./models/lookup.model";
import { LoaderService } from "./service/loader.service";
import { GeoLocationService } from "./service/geo-location.service";
import { LocationModel } from "./models/location.model";
import { LocationEntity } from "./entity/location.entity";
import { MatSlideToggleChange } from "@angular/material/slide-toggle";
import { MatDialog } from '@angular/material/dialog';
import { GeoInputComponent } from "./components/geo-input/geo-input.component";
import { ActivatedRoute, Router } from "@angular/router";

export enum QueryMode {
  IP = "ip",
  GPS = "gps"
}

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
  modes: QueryMode[] = [QueryMode.GPS, QueryMode.IP];
  messages: string[] = [];
  icons: string[] = ['location_disabled', 'my_location'];
  $background = this.api.$background;
  $lookup = this.api.$lookup;
  $location = this.api.$location;

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
          (new URL(this.router.url)).pathname == "" &&
          this.router.navigate(['ip', msg.content]);
      }
      if (msg.command === WSCommand.IP) {
        this.messages.push("IP");
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
      console.log(res);
    })
    // const params = window.location.search;
    // this.router.routerState.root.fragment.subscribe((res) => {
    //   console.log(res);
    // });
    // const ip = params.get("ip");
    // ip && this.updateGeoIP(ip);
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
        // this.currentLocation &&
        //   this.currentLocation?.renewBackground() &&
        //   this.backgroundSubject.next(this.currentLocation?.background)
        break;

      case this.queryMode.IP:
        // this.currentLookup &&
        //   this.currentLookup.renewBackground() &&
        //   this.backgroundSubject.next(this.currentLookup.background);
        break;
    }
  }
  onFullView() {
    this.fullview = !this.fullview;
  }




  async onModeSwitch($event: MatSlideToggleChange) {
    this.mode = this.modes.shift() as QueryMode;
    this.modes.push(this.mode);
    switch (this.mode) {
      case this.queryMode.GPS:
        this.geoService.getCurrentPosition().subscribe({
          next: (res: GeolocationPosition) => {
            console.debug(res);
            this.router.navigate(["location", `${res.coords.latitude},${res.coords.longitude}`]);
          }, error: (err: GeolocationPositionError) => {
            console.error(err);
            this.snackBar
              .open(err.message, "Ok", { duration: 2000, panelClass: 'warn' });
          }
        });
        break;
      case this.queryMode.IP:
        this.currentLookup && this.router.navigate(["ip", this.currentLookup.ip]);
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
      // hasBackdrop: true,
      autoFocus: 'dialog',
      maxWidth: '800px',
      width: '80vw',
      // data: input,
    });
    dialogRef.afterClosed().subscribe((input) => {
      console.log(input);
      // this.searching = false;
      if (input) {
        this.router.navigate(["location", input]);
        // this.mode = this.queryMode.GPS;
        // this.updateAddress(input);
        // const msg: WSRequest = {
        //   ztype: WSType.REQUEST,
        //   query: input,
        //   client: this.ws.DEVICE_ID,
        //   group: this.ws.DEVICE_ID,
        //   id: uuidv4(),
        // };
        // this.ws.send(msg);
      }
    });
  }

  title = "geo";
}
