import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {authGuard} from "../auth/middleware/auth.guard";
import {MenuComponent} from "./views/menu/menu.component";
import {IndexComponent} from "./views/index/index.component";
import {GameComponent} from "./views/game/game.component";
import {LobbyComponent} from "./views/lobby/lobby.component";

const routes: Routes = [

  { path: '',  title: "Home", component: IndexComponent,   canActivate: [authGuard],
    children: [
    { path: 'lobby',  title: "Lobby", component: LobbyComponent, outlet: "pokeroutlet",  canActivate: [authGuard]},
    { path: 'game',  title: "Game", component: GameComponent, outlet: "pokeroutlet",  canActivate: [authGuard]},
    { path: 'menu',  title: "Menu", component: MenuComponent, outlet: "pokeroutlet",  canActivate: [authGuard]},
  ]}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PokerRoutingModule { }
