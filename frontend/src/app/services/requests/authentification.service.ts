import {Inject, Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient, HttpInterceptor} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class AuthentificationService {

  constructor(private http: HttpClient, @Inject("BASE_URL") private baseUrl: string) { }

  // endpoint that checks if the user is authenticated; Post request to the server
  public testConnection(): Observable<string>{
    return this.http.get<string>(this.baseUrl);
  }
}
