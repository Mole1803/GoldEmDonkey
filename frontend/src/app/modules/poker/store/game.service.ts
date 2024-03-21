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

  //public game: GameDto;
  /*
  public cardList: CardDto[];
  public */


  constructor(@Inject("SOCKET_IO") public socketIo: string, public gameHttpService: GameHttpService, private userManagementService: UserManagementService, private router: Router) {
    console.log("constructor", socketIo)
    //this.init()
  }

  disconnect() {
    this.socket.disconnect();
  }


  joinGameHttp(gameId: string)
  {
    this.gameHttpService.joinGame(gameId, this.username ).subscribe(
      () => {
       }
    );
  }

  initializeGame() {
    this.username = this.userManagementService.getUser()


    setTimeout(()=> {
    this.socket.on("connect_error", (err: any) => {
      // the reason of the error, for example "xhr poll error"
      console.log(err.message);
      console.log(err)

      // some additional description, for example the status code of the initial HTTP response
      console.log(err.description);

      // some additional context, for example the XMLHttpRequest object
      console.log(err.context);
    });
    },10000)
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
       console.log("Instruction received", instruction);
      if(instruction.gamestate === 0){
        this.endOfRound.emit();

      }
      if(instruction.gamestate === 1){
        this.clientAtMove.emit();
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

  initializeJoinGame(){
    let gameJoined = new Observable<{player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}>(observer => {
      this.socket.on("joinedGame", (data: any) => {
        console.log("gameJoined", data);
        observer.next(data)
      })
    })

    gameJoined.subscribe((data: {player: PlayerDto, players: PlayerDto[], gameId: string, game: GameDto}) => {
      this.game = data.game
      this.playerList = data.players
      console.log("Received data in gameJoined Observable: ", data, data.players);
      this.gameJoined.emit(data!.player as PlayerDto)
    });
  }


  initializeGameStarted(){
    let gameStarted = new Observable(observer => {
      this.socket.on("startGame", () => {
        observer.next();
      })});

    gameStarted.subscribe(() => {
      console.log("Game started");
      // redirect to game view
      this.router.navigate([{outlets: {pokeroutlet: ['game']}}]);

      this.gameUpdated.emit();
    });
  }

  initializePerformInstruction(){
    let instruction = new Observable<{gamestate: number, kwargs: {}}>(observer => {
      this.socket.on("instruction", (instruction: {gamestate: number, kwargs: {}}) => {
        console.log("instruction", instruction);
        observer.next(instruction);
      })
    })




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



  initializeOnAny(){
    let onAny = new Observable(observer => {
      this.socket.onAny((event, ...args) => {
        console.log(`Socket Event: ${event}`);
        for (const arg of args) {
            console.log(`Arg: ${JSON.stringify(arg)}`);
        }
      });
    }
    )

    onAny.subscribe(() => {
      console.log("onAny");
    })
  }

  initializeOnConnectAndDisconnect(){
    let onConnect = new Observable(observer => {
      this.socket.on('connect', () => {
        console.log('Connected to the server');
        observer.next();
      });
    }
    )

    onConnect.subscribe(() => {
      console.log("onConnect");
    })

    let onDisconnect = new Observable(observer => {
      this.socket.on('disconnect', () => {
        console.log('Disconnected from the server');
        observer.next();
      });
    }
    )

    onDisconnect.subscribe(() => {
      console.log("onDisconnect");
    })

  }





  public initializeObservers(): void {
    this.initializeJoinGame();
    this.initializeGameStarted();
    this.initializePerformInstruction();
    this.initializeOnAny();
    this.initializeOnConnectAndDisconnect();
    console.log("observers initialized")
    /*let gameUpdated = new Observable(observer => {
      this.socket.on("performNextAction", (game: GameDto) => {
        // Get Status of the round
        console.log("performNextAction", game);
        observer.next(game);
      })
    });*/


  }



  public joinGame(gameId: string): void {
    /*if(this.game !== undefined && this.game!.id !== gameId){
      this.socket.disconnect()
      this.game = undefined
      this.socket = io.connect(this.socketIo)

    }*/

    /*if(this.socket.connected)
    {
      console.log("Socket connected");
      return
    }*/

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
    this.socket.emit("performRaise",{gameId: this.game!.id, username: this.username, bet: amount});
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
    return player.id === this.username;
  }
  // endregion ------------------------------

}
