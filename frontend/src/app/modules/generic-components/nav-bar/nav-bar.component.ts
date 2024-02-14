import { Component } from '@angular/core';
import {AuthStore} from "../../auth/store/auth-store";

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent {

  logout() {
    AuthStore.logout()
  }

}
