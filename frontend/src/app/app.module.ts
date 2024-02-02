import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {environment} from "../environments/environment";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import { LoginComponent } from './views/login/login.component';
import {FormsModule} from "@angular/forms";
import { RegistrationComponent } from './views/registration/registration.component';
import { MenuComponent } from './views/menu/menu.component';
import { RoomComponent } from './views/room/room.component';
import { WaitingroomComponent } from './views/waitingroom/waitingroom.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistrationComponent,
    MenuComponent,
    RoomComponent,
    WaitingroomComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    { provide: "BASE_URL", useValue: environment.BASE_URL },

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
