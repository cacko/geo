import { Injectable } from "@angular/core";
import { now, random } from "lodash-es";
import { interval, Observable, Observer, timer } from 'rxjs';
import { Subject } from 'rxjs';
import { v4 as uuidv4 } from 'uuid';
import { WSCommand, WSConnection, WSMessage } from "../entity/websockets.entiity";



@Injectable()
export class WebsocketService {

  private out: Observer<MessageEvent<any>> | undefined;
  private in: Observable<MessageEvent<any>> | undefined;

  private reconnectAfter = 0;
  private readonly RECONNECT_START = 2000;

  private messagesSubject = new Subject<WSMessage>();
  messages = this.messagesSubject.asObservable();

  constructor() {
    this.connect();
  }

  get URL(): string {
    return `${WSConnection.WS_URL}/${this.DEVICE_ID}`;
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
    interval(5000 + random(1000,5000)).subscribe((n) => {
      this.send({
        command: WSCommand.PING,
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
      console.debug("Successfully REconnected: " + this.URL);
    } catch (err) {
      console.error("Reconnect error", err);

    }
  }

  private create(url: string | URL): void {
    let ws = new WebSocket(url);
    ws.onmessage = (msg) => {
      console.info(msg.data)
      try {
        this.messagesSubject.next(JSON.parse(msg.data));
      } catch (err) {
        
      }

    };
    ws.onerror = (err) => {
      console.error(err);
      timer(this.reconnectAfter).subscribe(() => {
        this.reconnect();
        this.reconnectAfter += this.reconnectAfter * 0.1;
      });
    };
    ws.onclose = () => {
      this.reconnectAfter = this.RECONNECT_START;
    };
    this.out = {
      error: (err: any) => { console.debug(err); },
      complete: () => { },
      next: (data: Object) => {
        console.debug('Message sent to websocket: ', data);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      }
    };
  }
}