import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PokerRoutingModule } from './poker-routing.module';
import { IndexComponent } from './views/index/index.component';
import { GameComponent } from './views/game/game.component';
import { LobbyComponent } from './views/lobby/lobby.component';
import { MenuComponent } from './views/menu/menu.component';
import {GenericComponentsModule} from "../generic-components/generic-components.module";
import {GameService} from "./store/game.service";
import { ActionModalComponent } from './components/action-modal/action-modal.component';
import {NgSelectModule} from "@ng-select/ng-select";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {io} from "socket.io-client";
import {environment} from "../../../environments/environment";


@NgModule({
  declarations: [
    IndexComponent,
    GameComponent,
    LobbyComponent,
    MenuComponent,
    ActionModalComponent
  ],
  imports: [
    CommonModule,
    PokerRoutingModule,
    GenericComponentsModule,
    NgSelectModule,
    FormsModule,
    ReactiveFormsModule

  ],
  providers: [
    GameService,
    { provide: "SOCKET_IO", useValue: environment.BASE_URL}
  ]
})
export class PokerModule { }
