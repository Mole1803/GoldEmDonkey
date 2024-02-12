import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {environment} from "../environments/environment";
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import { RegistrationComponent } from './views/registration/registration.component';
import { MenuComponent } from './views/menu/menu.component';
import { RoomComponent } from './views/room/room.component';
import { WaitingroomComponent } from './views/waitingroom/waitingroom.component';
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import {AuthModule} from "./modules/auth/auth.module";

@NgModule({
  declarations: [
    AppComponent,
    RegistrationComponent,
    MenuComponent,
    RoomComponent,
    WaitingroomComponent,
    NavBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    AuthModule
  ],
  providers: [
    { provide: "BASE_URL", useValue: environment.BASE_URL },
    ],
  bootstrap: [AppComponent]
})
export class AppModule { }
