import {EventEmitter, Inject, Injectable} from '@angular/core';
import * as io from "socket.io-client";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";
import {GameHttpService} from "../services/game-http.service";
import {UserManagementService} from "../services/user-management.service";
import {PlayerDto} from "../models/player-dto";
import {Router} from "@angular/router";

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


  constructor(@Inject("SOCKET_IO") private socketIo: string, public gameHttpService: GameHttpService, private userManagementService: UserManagementService, private router: Router) {


    // Todo check if player is in a game
  }

  initializeGame() {
    this.username = this.userManagementService.getUser()
    this.socket = io.connect(this.socketIo)
    this.initializeObservers()
  }

    /**
   * Check if the player is this client
   * @param player
   */

  public createGame(): void {
    this.gameHttpService.createGame().subscribe(
      (game: GameDto) => {
        console.debug("Game created", game);
        this.game = game;
      }
    );
  }

  isSocketConnected(): boolean {
    return this.socket.connected;
  }

  public userHasActiveGame(): boolean {
    this.gameHttpService.hasActiveGame().subscribe(
      (game: GameDto) => {
        this.game = game;
      }
    );
    return this.game !== undefined;
  }

  public initializeObservers(): void {
    let gameJoined = new Observable<{player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}>(observer => {
      this.socket.on("joinGame", (data: any) => {
        console.log("gameJoined", data);
        observer.next(data);
      })
    });

    let gameStarted = new Observable(observer => {
      this.socket.on("startGame", () => {
        observer.next();
      })});


    let gameUpdated = new Observable(observer => {
      this.socket.on("performNextAction", (game: GameDto) => {
        // Get Status of the round
        console.log("performNextAction", game);
        observer.next(game);
      })
    });

    let instruction = new Observable<{gamestate: number, kwargs: {}}>(observer => {
      this.socket.on("instruction", (instruction: {gamestate: number, kwargs: {}}) => {
        console.log("instruction", instruction);
        observer.next(instruction);
      })
    })

    gameJoined.subscribe((data: {player: PlayerDto, players: PlayerDto[], gameId: string, game: GameDto}) => {
        this.gameJoined.emit(data!.player as PlayerDto)
        this.game = data.game
        this.playerList = data.players
      console.log("Received data in gameJoined Observable: ", data, data.players);
        console.log("Received data in gameJoined Observable: ", data, data.player);
    });

    gameStarted.subscribe(() => {
      console.log("Game started");
      // redirect to game view
      this.router.navigate([{outlets: {pokeroutlet: ['game']}}]);

      this.gameUpdated.emit();
    });

    instruction.subscribe((instruction: {gamestate: number, kwargs: {}}) => {
      console.log("Instruction received", instruction);
      if(instruction.gamestate === 0){
        this.endOfRound.emit();

      }
      if(instruction.gamestate === 1){
        this.clientAtMove.emit();
      }
    })
  }

  public joinGame(gameId: string): void {
    console.log("Joining game", gameId, this.username)
    if (!this.socket.connected || this.username === undefined || gameId === "" || gameId === undefined) {
      console.log("Socket not connected");
      return;
    }
    this.socket.emit("joinGame", {
      gameId: gameId,
      username: this.username
    });
  }

  runNextMove(){


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

  startGame(){
    this.socket.emit("startGame" ,{gameId: this.game!.id} );
  }



  // region Utils --------------------------
    isPlayerMoveClient(player: PlayerDto): boolean {
    return player.id === this.username;
  }
  // endregion ------------------------------

}
