import { Component } from '@angular/core';
import {Routing} from "../../enum/routing";
import {AuthStore} from "../../store/auth-store";
import {Router} from "@angular/router";
import {AuthHttpService} from "../../service/auth-http.service";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent {
  username: string = "";
  password: string = "";
  confirm_password: string = "";
  authStore?: AuthStore;

  constructor(private authHttpService: AuthHttpService, private router: Router){
    this.authStore = new AuthStore(authHttpService, router);
  }

  register(username: string, password: string, confirm_password: string) {
    if(username == "" || password == "") return
    if(password !== confirm_password) return
    this.authStore?.register(username, password, (success) => {
      if(success) {
        this.authStore?.redirectToHome();
      }
    }
    );
  }


  redirectToLogin() {
    return ["/"+Routing.Login];
  }


}
