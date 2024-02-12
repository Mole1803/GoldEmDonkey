import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PokerRoutingModule } from './poker-routing.module';
import { IndexComponent } from './views/index/index.component';
import { GameComponent } from './views/game/game.component';
import { LobbyComponent } from './views/lobby/lobby.component';
import { MenuComponent } from './views/menu/menu.component';
import {GenericComponentsModule} from "../generic-components/generic-components.module";


@NgModule({
  declarations: [
    IndexComponent,
    GameComponent,
    LobbyComponent,
    MenuComponent
  ],
  imports: [
    CommonModule,
    PokerRoutingModule,
    GenericComponentsModule
  ]
})
export class PokerModule { }
