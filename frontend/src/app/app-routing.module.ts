import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {authGuard} from "./modules/auth/middleware/auth.guard";
import {IndexComponent} from "./modules/poker/views/index/index.component";

const routes: Routes = [
  { path: 'home',  title: "Home", loadChildren: () => import('./modules/poker/poker.module').then(m => m.PokerModule),   canActivate: [authGuard]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true, enableTracing: true})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
