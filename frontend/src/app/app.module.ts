import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {environment} from "../environments/environment";
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {AuthModule} from "./modules/auth/auth.module";
import {GenericComponentsModule} from "./modules/generic-components/generic-components.module";
import {PokerModule} from "./modules/poker/poker.module";
import {CustomUrlSerializer} from "./utils/custom-url-serializer";
import {UrlSerializer} from "@angular/router";
import {io} from "socket.io-client";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    AuthModule,
    GenericComponentsModule,
    PokerModule,
    FormsModule
  ],
  providers: [
    { provide: UrlSerializer, useClass: CustomUrlSerializer },
    { provide: "BASE_URL", useValue: environment.BASE_URL },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
