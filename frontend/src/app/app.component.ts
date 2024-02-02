import {Component, OnInit} from '@angular/core';
import {AuthentificationService} from "./Services/requests/authentification.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'frontend';
  constructor(private authentificationService: AuthentificationService,) {
  }

  ngOnInit(): void {
    this.authentificationService.testConnection().subscribe(
      data => {
        console.log(data);
      }
    )
  }

}
