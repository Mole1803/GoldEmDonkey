import {JwtHeaderKey} from "../enum/jwt-header-key";

export class TokenHandler {
  static saveToken(jwt: string) {
    localStorage.setItem(JwtHeaderKey.JWT_TOKEN, jwt);
  }

  static getToken(): string | null {
    return localStorage.getItem(JwtHeaderKey.JWT_TOKEN);
  }

  static removeToken() {
    localStorage.removeItem(JwtHeaderKey.JWT_TOKEN);
  }
}
