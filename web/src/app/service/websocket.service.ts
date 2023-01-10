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
  private subject: AnonymousSubject<MessageEvent> | undefined;
  public messages: Subject<Message>;
  private ws: WebSocket | undefined;

  constructor() {
    this.messages = <Subject<Message>>this.connect().pipe(
      map(
        (response: MessageEvent): Message => {
          console.log(response.data);
          let data = JSON.parse(response.data)
          return data;
        }
      )
    );
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

  public connect(): AnonymousSubject<MessageEvent> {
    if (!this.subject) {
      this.subject = this.create(this.URL);
      console.log("Successfully connected: " + this.URL);
    }
    return this.subject;
  }

  public reconnect() {
    try {
      this.subject = this.create(`${this.URL}`);
      console.log("Successfully REconnected: " + this.URL);
    } catch (err) {
      console.error("RECON", err);
      setTimeout(() => this.reconnect(), 2000);
    }
  }

  private create(url: string | URL): AnonymousSubject<MessageEvent> {
    let ws = new WebSocket(url);
    let observable = new Observable((obs: Observer<MessageEvent>) => {
      ws.onmessage = obs.next.bind(obs);
      ws.onerror = obs.error.bind(obs);
      ws.onclose = () => {
        this.reconnect();
      };
      return ws.close.bind(ws);
    });
    let observer = {
      error: (err: any) => { console.log(err); },
      complete: () => { console.log("COMPLETEEEEEE") },
      next: (data: Object) => {
        console.log('Message sent to websocket: ', data);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      }
    };
    return new AnonymousSubject<MessageEvent>(observer, observable);
  }
}