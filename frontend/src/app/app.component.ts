import {Component, OnInit} from '@angular/core';
import {AuthHttpService} from "./modules/auth/service/auth-http.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'frontend';
  constructor(private authentificationService: AuthHttpService) {
  }

  ngOnInit(): void {
    /*this.authentificationService.testConnection().subscribe(
      data => {
        console.log(data);
      }
    )*/
  }

}
