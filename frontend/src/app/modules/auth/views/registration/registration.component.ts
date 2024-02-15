import { Component } from '@angular/core';
import {Routing} from "../../enum/routing";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent {
  username: string = "";
  password: string = "";
  confirm_password: string = "";

  register(username: string, password: string, confirm_password: string) {
    if(username == "" || password == "") return
    if(password !== confirm_password) return
    //TODO: redirect to home and save token
  }

  saveToken(jwt: any) {
    localStorage.setItem("token", jwt.access_token);
  }

  redirectToLogin() {
    return ["/"+Routing.Login];
  }


}
