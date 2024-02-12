import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { GameListComponent } from './game-list/game-list.component';



@NgModule({
    declarations: [
        NavBarComponent,
        GameListComponent
    ],
    exports: [
        NavBarComponent
    ],
    imports: [
        CommonModule
    ]
})
export class GenericComponentsModule { }
