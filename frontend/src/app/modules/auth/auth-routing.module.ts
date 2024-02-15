import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from "./views/login/login.component";
import {RegistrationComponent} from "./views/registration/registration.component";
import {Routing} from "./enum/routing";

const routes: Routes = [
  {path: Routing.Login, title: "Login", component: LoginComponent},
  {path: Routing.Register,title: "Registration", component: RegistrationComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
