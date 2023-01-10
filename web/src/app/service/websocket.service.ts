import { Injectable } from "@angular/core";
import { interval, Observable, Observer, Subscription } from 'rxjs';
import { AnonymousSubject } from 'rxjs/internal/Subject';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { v4 as uuidv4 } from 'uuid';
import { now } from 'lodash-es';

const WS_URL = "wss://geo.cacko.net/ws";

export interface Message {
  source: string;
  content: string;
}

@Injectable()
export class WebsocketService {

  private out: Observer<MessageEvent<any>> | undefined;
  private in: Observable<MessageEvent<any>> | undefined;

  private messagesSubject = new Subject<Message>();
  messages = this.messagesSubject.asObservable();

  constructor() {
    this.connect();
  }

  get URL(): string {
    return `${WS_URL}/${this.DEVICE_ID}`;
  }

  get DEVICE_ID(): string {
    let id = localStorage.getItem('device_id');
    if (!id) {
      id = uuidv4();
      localStorage.setItem('device_id', id);
    }
    return id;
  }

  public connect() {
    this.create(this.URL);
    console.log("Successfully connected: " + this.URL);
    interval(5000).subscribe((n) => {
      this.send({
        source: "PING",
        content: `${now()}`
      });
    })
  }

  public send(data: any) {
    this.out?.next(data);
  }

  public reconnect() {
    try {
      this.create(`${this.URL}`);
      console.log("Successfully REconnected: " + this.URL);
    } catch (err) {
      console.error("RECON", err);
      setTimeout(() => this.reconnect(), 2000);
    }
  }

  private create(url: string | URL): void {
    let ws = new WebSocket(url);
    this.in = new Observable((obs: Observer<MessageEvent>) => {
      ws.onmessage = (msg) => {
        const data = msg as unknown as Message;
        this.messagesSubject.next(data);
      };
      ws.onerror = obs.error.bind(obs);
      ws.onclose = () => {
        this.reconnect();
      };
      return ws.close.bind(ws);
    });
    this.out = {
      error: (err: any) => { console.log(err); },
      complete: () => { console.log("COMPLETEEEEEE") },
      next: (data: Object) => {
        console.log('Message sent to websocket: ', data);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      }
    };
  }
}