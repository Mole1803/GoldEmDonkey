export class GameDto {
  id: string
  isActive: boolean

  constructor(id: string, isActive: boolean) {
    this.id = id
    this.isActive = isActive
  }
}
