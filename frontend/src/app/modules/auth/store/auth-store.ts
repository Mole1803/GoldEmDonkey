import {AuthHttpService} from "../service/auth-http.service";
import {TokenHandler} from "../utils/token-handler";

  /**
   * Uses the LocalStorage to save the JWT_TOKEN
   * @param authHttpService
   */
export class AuthStore {

  constructor(private authHttpService: AuthHttpService) {}


  /**
    * Logs the user in and saves the JWT_TOKEN in the LocalStorage
    * @return true if the login was successful
   */
  async login(username: string, password: string, callback: (success: boolean) => void) {
    this.authHttpService.login(username, password).subscribe(jwt => {
      TokenHandler.saveToken(jwt);
      callback(true);
    }
    );
  }

  async register(username: string, password: string, callback: (success: boolean) => void) {
    this.authHttpService.register(username, password).subscribe(jwt => {
      TokenHandler.saveToken(jwt);
      callback(true);
    }
    );
  }

  async isUsernameAvailable(username: string, callback: (available: boolean) => void) {
    this.authHttpService.isUsernameAvailable(username).subscribe(available => {
      callback(available);
    }
    );
  }


  static logout() {
    TokenHandler.removeToken();
    window.location.reload();
    // Todo: reload the page or redirect to land on the login page
  }


}
