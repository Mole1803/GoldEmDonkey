import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { GameListComponent } from './game-list/game-list.component';
import {RouterLink, RouterLinkActive} from "@angular/router";



@NgModule({
    declarations: [
        NavBarComponent,
        GameListComponent
    ],
    exports: [
        NavBarComponent
    ],
  imports: [
    CommonModule,
    RouterLinkActive,
    RouterLink
  ]
})
export class GenericComponentsModule { }
