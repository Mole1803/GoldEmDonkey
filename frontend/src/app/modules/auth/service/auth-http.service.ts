import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthHttpService {

    constructor(private http: HttpClient, @Inject("BASE_URL") private baseUrl: string) { }

  // endpoint that checks if the user is authenticated; Post request to the server
  public testConnection(): Observable<string>{
    return this.http.get<string>(this.baseUrl);
  }
}
