import {CanActivateFn, Router} from '@angular/router';
import {inject} from "@angular/core";
import {AuthService} from "../service/auth.service";
import {Routing} from "../enum/routing";

export const authGuard: CanActivateFn = (route, state) => {
    const authService = inject(AuthService)
  const router = inject(Router)
  if(authService.isAuthenticated()){
    return true
  }
  // TODO: set route
  return router.parseUrl("/"+Routing.Login)
};
