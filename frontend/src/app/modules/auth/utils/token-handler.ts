import {JwtHeaderKey} from "../enum/jwt-header-key";

export class TokenHandler {
  static saveToken(jwtObject: any) {
    // currently stores [object Object] in local storage store dict instead
    const jwt = jwtObject.access_token as string;
    localStorage.setItem(JwtHeaderKey.JWT_TOKEN, jwt);
  }

  static storeUser(user: string) {
    localStorage.setItem('user', user);

  }

  static getToken(): string | null {
    return localStorage.getItem(JwtHeaderKey.JWT_TOKEN);
  }

  static removeToken() {
    localStorage.removeItem(JwtHeaderKey.JWT_TOKEN);
  }
}
