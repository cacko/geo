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
      switch(msg.command)  {
        case WSCommand.IP:
          if (!this.ownIP) {
            this.ownIP = msg.content;
          }
          return this.isIPChanged(msg.content) && this.updateGeoIP(msg.content);
      }
      if (msg.command === WSCommand.IP) {
        this.messages.push(msg.content);
      }
    });
  }

  updateGeoIP(new_ip: string) {
    this.ownIP= new_ip;
  }

  get ownIP(): string | null {
    return localStorage.getItem(this.KEY_OWN_IP);
  }

  set ownIP(ip: string | null) {
    localStorage.setItem(this.KEY_OWN_IP, ip || "");
  }

  isIPChanged(current_ip: string): boolean {
    return current_ip !== this.ownIP;
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
    this.api.fetch(ApiType.LOOOKUP, { ip: params.get("ip") }).then((res) => {
      this.lookup = res as LookupEntity;
    }).catch((err) => {

    });
  }
  title = 'geo';

}