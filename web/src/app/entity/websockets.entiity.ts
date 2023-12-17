
export enum WSConnection {
  WS_URL = "wss://geo.cacko.net/ws"
}

export enum WSCommand {
  IP = "ip",
  PING = "ping",
  LOOKUP = "lookup",
  BACKGROUND = "background",
  STYLES = "styles"
}



export interface WSMessage {
  command: string;
  content: string[];
}
