import { Component } from '@angular/core';
import {AuthStore} from "../../auth/store/auth-store";
import {Router} from "@angular/router";

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent {
  constructor(private router: Router) { }

  logout() {
    AuthStore.logout()
  }

  redirectToGame(){
    // outlet is pokeroutlet in poker-routing.module.ts
    this.router.navigate([{outlets: {pokeroutlet: ['game']}}]);

  }
}
