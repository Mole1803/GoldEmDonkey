import {EventEmitter, Inject, Injectable} from '@angular/core';
import * as io from "socket.io-client";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";
import {GameHttpService} from "../services/game-http.service";
import {UserManagementService} from "../services/user-management.service";
import {PlayerDto} from "../models/player-dto";
import {Router} from "@angular/router";
import {Socket} from "socket.io-client";

@Injectable({
  providedIn: 'root'
})
export class GameService {
  public socket!: Socket;
  public game?: GameDto
  public username!: string;


  gameJoined: EventEmitter<PlayerDto> = new EventEmitter<PlayerDto>()
  gameUpdated: EventEmitter<void> = new EventEmitter<void>()
  endOfRound: EventEmitter<void> = new EventEmitter<void>()
  clientAtMove: EventEmitter<void> = new EventEmitter<void>()
  gameCreated: EventEmitter<string> = new EventEmitter<string>()
  public playerList: PlayerDto[] = [];
  public gameData!: {gamestate: number, kwargs: {}}
  //public game: GameDto;
  /*
  public cardList: CardDto[];
  public */


  constructor(@Inject("SOCKET_IO") public socketIo: string, public gameHttpService: GameHttpService, private userManagementService: UserManagementService, private router: Router) {
    console.log("constructor", socketIo)
    //this.init()
  }

  disconnect() {
    if(this.socket !== undefined && this.socket.connected)
      this.socket.disconnect();
  }

  init(){
    this.socket =  io.connect(this.socketIo)

    this.username = this.userManagementService.getUser()
    this.socket.on("connect", () => {
      console.log("init")
      this.socket.on("joinedGame", (data: {player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}) => {
        console.log("gameJoined", data);
        this.gameJoinedFn(data)
      });
      this.socket.on("startGame", () => {
        console.log("Game Started received")
        this.gameStartedFn()
      })

      this.socket.on("instruction", (instruction: {gamestate: number, kwargs: {}}) => {
        console.log("instruction", instruction);
        this.instructionFn(instruction)
      })
    });
  }


  gameJoinedFn(data:  {player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}){
      console.log("gameJoined", data)
      this.game = data.game
      this.playerList = data.players

  }

  gameStartedFn(){
    this.router.navigate([{outlets: {pokeroutlet: ['game']}}]);
  }

  instructionFn(instruction: {gamestate: number, kwargs: {}}){
      console.log("Instruction received 1", instruction);
      this.gameData=instruction
      if(instruction.gamestate > 3){
        this.endOfRound.emit();

      }
      if(instruction.gamestate >-1  && instruction.gamestate<4){
        this.clientAtMove.emit();
        this.gameUpdated.emit();
        // is current player
        // @ts-ignore
        let activePlayer = instruction["kwargs"]["nextPlayer"]! as PlayerDto
        if(this.isPlayerMoveClient(activePlayer)){
          this.clientAtMove.emit()
        }
      }

  }

    /**
   * Check if the player is this client
   * @param player
   */

  public createGame(gameName: string): void {
    this.gameHttpService.createGame(gameName).subscribe(
      (game: GameDto) => {
        console.debug("Game created", game);
        this.game = game;
        this.gameCreated.emit(game.id);
      }
    );
  }

  /*public userHasActiveGame(): boolean {
    this.gameHttpService.hasActiveGame().subscribe(
      (game: GameDto) => {
        this.game = game;
      }
    );
    return this.game !== undefined;
  }*/



  public joinGame(gameId: string): void {
    if ( this.username === undefined || gameId === "" || gameId === undefined) {
      console.log("Socket not connected");
      return;
    }
    console.log("Joining game", gameId, this.username)

    this.socket.emit("joinGame", {
      gameId: gameId,
      username: this.username
    })
  }


  public sendPerformFold(): void {
    console.log("Performing fold");
    this.socket.emit("performFold", {gameId: this.game!.id, username: this.username});
  }

  public sendPerformCheck(): void {
    console.log("Performing check");
    this.socket.emit("performCheck",{gameId: this.game!.id, username: this.username});
  }

  public sendPerformCall(): void {
    console.log("Performing call");
    this.socket.emit("performCall",{gameId: this.game!.id, username: this.username});
  }

  public sendPerformRaise(amount: number): void {
    console.log("Performing raise", amount);
    this.socket.emit("performRaise",{gameId: this.game!.id, username: this.username, raise_value: amount});
  }



  gameMove(action: string, player: PlayerDto) {
    /*if(!this.isPlayerMoveClient(player)){
      return;
    }*/

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
    console.log("Starting game", this.game!.id)
    this.socket.emit("startGame" ,{gameId: this.game!.id}, (res: any)=>{
      console.log(res)
    } );
  }



  // region Utils --------------------------
    isPlayerMoveClient(player: PlayerDto): boolean {
    console.log(player.userId, this.username)
    return player.userId === this.username;
  }
  // endregion ------------------------------

}
