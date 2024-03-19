import {AuthHttpService} from "../service/auth-http.service";
import {TokenHandler} from "../utils/token-handler";
import {AvailabilityCheckDto} from "../models/availability-check-dto";
import {Router} from "@angular/router";
import {Token} from "@angular/compiler";

  /**
   * Uses the LocalStorage to save the JWT_TOKEN
   * @param authHttpService
   */
export class AuthStore {

  constructor(private authHttpService?: AuthHttpService, private router?: Router) {}


  /**
    * Logs the user in and saves the JWT_TOKEN in the LocalStorage
    * @return true if the login was successful
   */
  async login(username: string, password: string, callback: (success: boolean) => void) {
    if(this.authHttpService === undefined) {
      console.error("AuthHttpService is not defined. Returning")
      return;
    }

    this.authHttpService?.login(username, password).subscribe(jwt => {
      console.log(jwt)
      TokenHandler.saveToken(jwt);
      TokenHandler.storeUser(username);

      callback(true);
    }, error => {
      callback(false);
    }
    );
  }

  async register(username: string, password: string, callback: (success: boolean) => void) {
    if(this.authHttpService === undefined) {
      console.error("AuthHttpService is not defined. Returning")
      return;
    }

    this.authHttpService?.register(username, password).subscribe(jwt => {
      TokenHandler.saveToken(jwt);
      callback(true);

    }, error => {
      callback(false);
      }
    );
  }

  async isUsernameAvailable(username: string, callback: (dto: AvailabilityCheckDto | undefined) => void) {
    if(this.authHttpService === undefined) {
      console.error("AuthHttpService is not defined. Returning")
      return;
    }
    this.authHttpService?.isUsernameAvailable(username).subscribe(response => {
      callback(response);
    },
    error => {
      callback(undefined);
    }
    );
  }


  static logout() {
    TokenHandler.removeToken();
    window.location.reload();
    // Todo: reload the page or redirect to land on the login page
  }

  redirectToHome() {
    if (this.router === undefined) {
      console.error("Router is not defined. Returning")
      return;
    }
    this.router.navigate(['/']);
  }
}
