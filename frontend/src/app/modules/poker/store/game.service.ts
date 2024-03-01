import {Inject, Injectable} from '@angular/core';
import * as io from "socket.io-client";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GameService {
  public socket: io.Socket;
  constructor(@Inject("SOCKET_IO") private socketIo: string){
    this.socket = io.connect(socketIo)
  }

  public initializeObservers(): void {
    let observer = new Observable(observer => {this.socket.on("gameJoined", (gameId: string) => {
      console.log("gameJoined", gameId);
      observer.next(gameId);
    })});

  }

  public joinGame(gameId: string): void {
    this.socket.emit("joinGame", gameId);
  }


}
