import { Component } from '@angular/core';
import {io} from "socket.io-client";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent {
  private socket = io('http://localhost:8080');

  testSocketIo() {
    this.socket.emit('message', 'Hello, World!');

  }
}
