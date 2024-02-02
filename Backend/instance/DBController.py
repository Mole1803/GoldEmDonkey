from Backend._DatabaseCall import db, User as UserDB
from Backend.Model.dto.Player import Player


def create_users_db(name, password, salt):
    ship = UserDB(
        name=name,
        password=password,
        salt=salt
    )
    try:
        db.session.add(ship)
        db.session.commit()
        return True
    except:
        return False
