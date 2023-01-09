import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent {

  status: boolean = false;
  changes: string[] = [];

  @Input() set online(status: boolean) {
    this.status = status;
    this.changes.push(status ? 'online' : 'offline');
  }

}
