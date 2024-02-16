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

}
