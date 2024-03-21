import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";
import {PlayerDto} from "../models/player-dto";

@Injectable({
  providedIn: 'root'
})
export class GameHttpService {


  constructor(private http: HttpClient, @Inject("BASE_URL") private baseUrl: string) { }

  public listActiveGames(): Observable<GameDto[]> {
    return this.http.get<GameDto[]>(this.baseUrl + "/game/listActiveGames");
  }

  public createGame(name: string): Observable<GameDto> {
    return this.http.post<GameDto>(this.baseUrl + "/game/createGame", {name: name});
  }

  public hasActiveGame(): Observable<GameDto> {
    return this.http.get<GameDto>(this.baseUrl + "/game/hasActiveGame");
  }


  public joinGame(gameId: string, username: string): Observable<{player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}> {
    return this.http.post<{player: PlayerDto, players: PlayerDto[], gameId:string, game: GameDto}>(this.baseUrl + "/game/joinGame", {gameId, username});
  }
}
