import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {authGuard} from "../auth/middleware/auth.guard";
import {MenuComponent} from "./views/menu/menu.component";
import {IndexComponent} from "./views/index/index.component";

const routes: Routes = [
  { path: '',  title: "Home", component: IndexComponent,  canActivate: [authGuard]},
  { path: 'lobby',  title: "Lobby", component: MenuComponent,  canActivate: [authGuard]},
  { path: 'game',  title: "Game", component: MenuComponent,  canActivate: [authGuard]},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PokerRoutingModule { }
