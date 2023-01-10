
export enum WSConnection {
  WS_URL = "wss://geo.cacko.net/ws"
}

export enum WSCommand {
  IP = "ip"
}

export interface WSMessage {
  command: string;
  content: string;
}
