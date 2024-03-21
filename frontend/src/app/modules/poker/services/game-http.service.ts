import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {GameDto} from "../models/game-dto";

@Injectable({
  providedIn: 'root'
})
export class GameHttpService {


  constructor(private http: HttpClient, @Inject("BASE_URL") private baseUrl: string) { }

  public listActiveGames(): Observable<GameDto[]> {
    return this.http.get<GameDto[]>(this.baseUrl + "/game/listActiveGames");
  }

  public createGame(): Observable<GameDto> {
    return this.http.post<GameDto>(this.baseUrl + "/game/createGame", {});
  }

  public hasActiveGame(): Observable<GameDto> {
    return this.http.get<GameDto>(this.baseUrl + "/game/hasActiveGame");
  }


  public joinGame(gameId: string, username: string): Observable<void> {
    return this.http.post<void>(this.baseUrl + "/game/joinGame", {gameId, username});
  }
}
