export class AvailabilityCheckDto {
  isUsernameAvailable: boolean;
  username: string;

  constructor(isUsernameAvailable: boolean, username: string) {
    this.isUsernameAvailable = isUsernameAvailable;
    this.username = username;
  }
}
