import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {AvailabilityCheckDto} from "../models/availability-check-dto";

@Injectable({
  providedIn: 'root'
})
export class AuthHttpService {

  constructor(private http: HttpClient, @Inject("BASE_URL") private baseUrl: string) { }

  // endpoint that checks if the user is authenticated; Post request to the server
  public testConnection(): Observable<string>{
    return this.http.get<string>(this.baseUrl);
  }

  public register(username: string, password: string): Observable<string> {
    return this.http.post<string>(this.baseUrl+"/auth/register", {username: username, password: password});
  }

  public login(username: string, password: string): Observable<string> {
    return this.http.post<string>(this.baseUrl+"/auth/login", {username: username, password: password});
  }

  public isUsernameAvailable(username: string): Observable<AvailabilityCheckDto> {
    return this.http.post<AvailabilityCheckDto>(this.baseUrl+"/auth/isUsernameAvailable", {username: username});
  }


}
