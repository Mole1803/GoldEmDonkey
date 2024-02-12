import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {environment} from "../environments/environment";
import {HTTP_INTERCEPTORS, HttpClient, HttpClientModule} from "@angular/common/http";
import { LoginComponent } from './views/login/login.component';
import {FormsModule} from "@angular/forms";
import { RegistrationComponent } from './views/registration/registration.component';
import { MenuComponent } from './views/menu/menu.component';
import { RoomComponent } from './views/room/room.component';
import { WaitingroomComponent } from './views/waitingroom/waitingroom.component';
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import { AuthInterceptor } from './interceptors/auth/auth.interceptor';
import {HashLocationStrategy, LocationStrategy} from "@angular/common";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
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
    FormsModule
  ],
  providers: [
    { provide: "BASE_URL", useValue: environment.BASE_URL },
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
