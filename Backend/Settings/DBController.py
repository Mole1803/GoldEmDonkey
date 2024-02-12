from Backend._DatabaseCall import db, RoundDB, GameDB, PlayerDB, RoundPlayerDB, CardsDB, RoundPlayerCardsDB, RoundCardsDB


def create_game_db(id):
    game = GameDB(
        id=id
    )
    try:
        db.session.add(game)
        db.session.commit()
        return True
    except:
        return False


def create_round_db(id, max_raise, game_id):
    round = RoundDB(
        id=id,
        max_raise=max_raise,
        game_id=game_id
    )
    try:
        db.session.add(round)
        db.session.commit()
        return True
    except:
        return False


def create_player_db(id, position, chips):
    player = PlayerDB(
        id=id,
        position=position,
        chips=chips
    )
    try:
        db.session.add(player)
        db.session.commit()
        return True
    except:
        return False


def create_round_player_db(id, id_round, id_player, at_play, set_chips):
    round_player = RoundPlayerDB(
        id=id,
        id_round=id_round,
        id_player=id_player,
        at_play=at_play,
        set_chips=set_chips
    )
    try:
        db.session.add(round_player)
        db.session.commit()
        return True
    except:
        return False


def create_card_db(id, color, value):
    card = CardsDB(
        id=id,
        color=color,
        value=value
    )
    try:
        db.session.add(card)
        db.session.commit()
        return True
    except:
        return False


def create_round_cards_db(id_round, id_cards, position):
    round_cards = RoundCardsDB(
        id_round=id_round,
        id_cards=id_cards,
        position=position
    )
    try:
        db.session.add(round_cards)
        db.session.commit()
        return True
    except:
        return False


def create_round_player_cards_db(id_round_player, id_cards):
    round_player_cards = RoundPlayerCardsDB(
        id_round_player=id_round_player,
        id_cards=id_cards
    )
    try:
        db.session.add(round_player_cards)
        db.session.commit()
        return True
    except:
        return False


def get_all_games():
    games = db.session.query(GameDB).all()
    returnList = []
    for game in games:
        returnList.append(game)
    return returnList


def set_max_raise_round(id, max_raise):
    round = db.session.query(RoundDB).filter_by(id=id).all()
    if len(round) == 0:
        return False
    round = round[0]
    round.max_raise = max_raise
    commit()


def set_chips_player(id, chips):
    player = db.session.query(PlayerDB).filter_by(id=id).all()
    if len(player) == 0:
        return False
    player = player[0]
    player.chips = chips
    commit()


def commit():
    try:
        db.session.commit()
        return True
    except:
        return False


def set_at_play(id, at_play):
    round_player = db.session.query(RoundPlayerDB).filter_by(id=id).all()
    if len(round_player) == 0:
        return False
    round_player = round_player[0]
    round_player.at_play = at_play
    commit()


def set_player_set_chips(id, set_chips):
    round_player = db.session.query(RoundPlayerDB).filter_by(id=id).all()
    if len(round_player) == 0:
        return False
    round_player = round_player[0]
    round_player.set_chips = set_chips
    commit()

