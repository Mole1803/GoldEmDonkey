import { Component } from '@angular/core';
import {Routing} from "../../enum/routing";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  password: string = "";
  username: string = "";

  async login(username: string, password: string) {}

  redirectToRegister() {
    return ['/'+Routing.Register];
  }

  protected readonly Routing = Routing;
}
