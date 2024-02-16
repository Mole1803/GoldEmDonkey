export class GameDto {
  id: string
  isActive: boolean
  hasStarted: boolean
  name: string

  constructor(id: string, isActive: boolean, hasStarted: boolean, name: string) {
    this.id = id
    this.isActive = isActive
    this.hasStarted = hasStarted
    this.name = name
  }
}
