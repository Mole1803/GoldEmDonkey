import {Inject, Injectable} from '@angular/core';
import * as io from "socket.io-client";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";
import {GameHttpService} from "../services/game-http.service";

@Injectable({
  providedIn: 'root'
})
export class GameService {
  public socket: io.Socket;
  public game?: GameDto

  //public game: GameDto;
  /*public playerList: PlayerDto[];
  public cardList: CardDto[];
  public */


  constructor(@Inject("SOCKET_IO") private socketIo: string, public gameHttpService: GameHttpService) {
    this.socket = io.connect(socketIo)

    // Todo check if player is in a game
  }

  public userHasActiveGame(): boolean {
    return this.game !== undefined;
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

  public createGame(): void {
    this.gameHttpService.createGame().subscribe(
      (game: GameDto) => {
        console.debug("Game created", game);
        this.game = game;

        // TOdo: join game
        //this.joinGame(game.id);
      }
    );
  }


}
