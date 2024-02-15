import { Component } from '@angular/core';
import {Routing} from "../../enum/routing";
import {AuthHttpService} from "../../service/auth-http.service";
import {AuthStore} from "../../store/auth-store";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  password: string = "";
  username: string = "";
  authStore?: AuthStore;

  constructor(private authHttpService: AuthHttpService, private router: Router){
    this.authStore = new AuthStore(authHttpService, router);
  }

  async login(username: string, password: string) {
    this.authStore?.login(username, password, (success) => {
      if(success) {
        this.authStore?.redirectToHome();
      }
    }
    );
  }

  redirectToRegister() {
    return ['/'+Routing.Register];
  }

  protected readonly Routing = Routing;
}
