import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  password: string = "";
  username: string = "";

  async login(username: string, password: string) {}



  redirectToRegister() {}

}
