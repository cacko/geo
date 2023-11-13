import { Component, NgZone, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SwUpdate } from '@angular/service-worker';
import { ApiType } from './entity/api.entity';
import { ApiService } from './service/api.service';
import { interval } from 'rxjs';
import { LookupEntity } from './entity/lookup.entity';
import { WebsocketService } from './service/websocket.service';
import { WSCommand } from './entity/websockets.entiity';
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
  online = true;

  messages: string[] = [];

  private readonly KEY_OWN_IP = "own-ip";

  constructor(
    private api: ApiService,
    private zone: NgZone,
    private swUpdate: SwUpdate,
    private ws: WebsocketService,
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
      this.zone.run(() => (this.loading = res));
    })

    this.ws.messages.subscribe((msg) => {
      switch (msg.command) {
        case WSCommand.IP:
          this.updateGeoIP(msg.content)
      }
      if (msg.command === WSCommand.IP) {
        this.messages.push(msg.content);
      }
    });
  }

  updateGeoIP(ip: string | null) {
    this.api.fetch(ApiType.LOOKUP, { path: ip }).then((res) => {
      this.lookup = res as LookupEntity;
    }).catch((err) => {

    });
  }

  sendMsg(source: string, content: string) {
    let message = {
      source,
      content
    };

    this.ws.send(message);
  }

  ngOnInit(): void {
    const params = new URLSearchParams(window.location.search);
    const ip = params.get("ip");
    ip && this.api.fetch(ApiType.LOOKUP, { path:  ip}).then((res) => {
      this.lookup = res as LookupEntity;
    }).catch((err) => {

    });
  }
  title = 'geo';
}