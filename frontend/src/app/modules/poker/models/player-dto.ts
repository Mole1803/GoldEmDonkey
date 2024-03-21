
export class PlayerDto {
    id: string;
    position: number;
    chips: number;
    gameId: string;
    userId: string

    constructor(id: string, position: number, chips: number, gameId: string, userId: string) {
        this.id = id;
        this.position = position;
        this.chips = chips;
        this.gameId = gameId;
        this.userId = userId;
    }
}
