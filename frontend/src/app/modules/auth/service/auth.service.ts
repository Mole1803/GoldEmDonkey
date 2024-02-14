import {Injectable} from '@angular/core';
import {jwtDecode} from 'jwt-decode'
import {TokenHandler} from "../utils/token-handler";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() {
  }

  public isAuthenticated(): boolean {
    const token = TokenHandler.getToken();

    if (typeof token === "string") {
      let jwtSplitted = token.split("\\.");
      if (jwtSplitted.length != 3) // The JWT is composed of three parts
        return true;// TODO set to False :: currently just for debugging purposes!!!
      let body = jwtDecode(token)
      if (Date.now() < body.exp! * 1000) {
        return true
      }
    }
    return false
  }
}
