import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {authGuard} from "./modules/auth/middleware/auth.guard";
import {MenuComponent} from "./views/menu/menu.component";

const routes: Routes = [
  { path: '',  title: "Home", component: MenuComponent,  canActivate: [authGuard]},
  //{ path: 'login', title: "Login",  component: LoginComponent},
  //{ path: 'register',  component: RegisterComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
