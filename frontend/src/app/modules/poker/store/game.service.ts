import {EventEmitter, Inject, Injectable} from '@angular/core';
import * as io from "socket.io-client";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";
import {GameHttpService} from "../services/game-http.service";
import {UserManagementService} from "../services/user-management.service";
import {PlayerDto} from "../models/player-dto";

@Injectable({
  providedIn: 'root'
})
export class GameService {
  public socket!: io.Socket;
  public game?: GameDto
  public username!: string;


  gameJoined: EventEmitter<PlayerDto> = new EventEmitter<PlayerDto>()
  gameUpdated: EventEmitter<void> = new EventEmitter<void>()
  endOfRound: EventEmitter<void> = new EventEmitter<void>()
  clientAtMove: EventEmitter<void> = new EventEmitter<void>()
  public playerList: PlayerDto[] = [];
  //public game: GameDto;
  /*
  public cardList: CardDto[];
  public */


  constructor(@Inject("SOCKET_IO") private socketIo: string, public gameHttpService: GameHttpService, private userManagementService: UserManagementService) {


    // Todo check if player is in a game
  }

  initializeGame() {
    this.username = this.userManagementService.getUser()
    this.socket = io.connect(this.socketIo)
    this.initializeObservers()
  }

  public userHasActiveGame(): boolean {
    return this.game !== undefined;
  }

  public initializeObservers(): void {
    let gameJoined = new Observable<{player: PlayerDto, players: PlayerDto[], room:string}>(observer => {
      this.socket.on("joinGame", (data: any) => {
        console.log("gameJoined", data);
        observer.next(data);
      })
    });

    let gameUpdated = new Observable(observer => {
      this.socket.on("performNextAction", (game: GameDto) => {
        // Get Status of the round
        console.log("performNextAction", game);
        observer.next(game);
      })
    });


    gameJoined.subscribe((data: {player: PlayerDto, players: PlayerDto[], room:string}) => {
        this.gameJoined.emit(data!.player as PlayerDto)
        this.playerList = data.players
      console.log("Received data in gameJoined Observable: ", data, data.players);
        console.log("Received data in gameJoined Observable: ", data, data.player);
    });

  }

  public joinGame(gameId: string): void {
    console.log("Joining game", gameId, this.username)
    this.socket.emit("joinGame", {
      gameId: gameId,
      username: this.username
    });
  }

  runNextMove(){


  }

  /**
   * Check if the player is this client
   * @param player
   */
  isPlayerMoveClient(player: PlayerDto): boolean {
    return player.id === this.username;
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

  public sendPerformFold(): void {
    this.socket.emit("performFold");
  }

  public sendPerformCheck(): void {
    this.socket.emit("performCheck");
  }

  public sendPerformCall(): void {
    this.socket.emit("performCall");
  }

  public sendPerformRaise(amount: number): void {
    this.socket.emit("performRaise", amount);
  }

  gameMove(action: string, player: PlayerDto) {
    if(!this.isPlayerMoveClient(player)){
      return;
    }

    switch (action) {
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
