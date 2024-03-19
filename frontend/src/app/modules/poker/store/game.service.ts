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
    this.initializeObservers()

    // Todo check if player is in a game
  }

  public userHasActiveGame(): boolean {
    return this.game !== undefined;
  }

  public initializeObservers(): void {
    let gameJoined = new Observable(observer => {this.socket.on("gameJoined", (gameId: string) => {
      console.log("gameJoined", gameId);
      observer.next(gameId);
    })});

    let gameUpdated = new Observable(observer => {this.socket.on("performNextAction", (game: GameDto) => {
      // Get Status of the round
      console.log("performNextAction", game);
      observer.next(game);
    })});


  }

  public joinGame(gameId: string): void {
    console.log("Joining game", gameId)
    this.socket.emit("joinGame", gameId);
  }

  public createGame(): void {
    this.gameHttpService.createGame().subscribe(
      (game: GameDto) => {
        console.debug("Game created", game);
        this.game = game;
        this.joinGame(this.game.id)

        // TOdo: join game
        //this.joinGame(game.id);
      }
    );
  }

  public sendPerformFold(): void{
    this.socket.emit("performFold");
  }

  public sendPerformCheck(): void{
    this.socket.emit("performCheck");
  }

  public sendPerformCall(): void{
    this.socket.emit("performCall");
  }

  public sendPerformRaise(amount: number): void{
    this.socket.emit("performRaise", amount);
  }

  gameMove(action: string, player: string){
    //if(this.player)

    switch(action){
      case "fold":
        this.sendPerformFold();
        break;
      case "check":
        this.sendPerformCheck();
        break;
      case "call":
        this.sendPerformCall();
        break;
      case "raise":
        this.sendPerformRaise(10);
        break;
      default:
        console.log("Invalid action");
    }
  }



}
