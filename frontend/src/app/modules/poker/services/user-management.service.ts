import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserManagementService {

  constructor() { }

  // get user from local storage (jwt)
  public getUser(): string {
    return localStorage.getItem('user')!;
  }
}
