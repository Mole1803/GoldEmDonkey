import os

from flask_sqlalchemy import SQLAlchemy

from Backend.Model.Login.LoginDto import LoginDto
from hashlib import sha256
from Backend._DatabaseCall import UserDB


class AuthService:
    @staticmethod
    def add_user(login: LoginDto, db_context: SQLAlchemy):
        if AuthService.username_exists(login=login, db_context=db_context):
            return None
        salt = AuthService.__create_salt()
        password = AuthService.hash_password(login.password, salt)

        user = UserDB(username=login.username, password=password, salt=salt)
        db_context.session.add(user)
        db_context.session.commit()
        return user

    @staticmethod
    def verify_user(login: LoginDto, db_context: SQLAlchemy):
        user = AuthService.__get_user_from_db(username=login.username, db_context=db_context)
        if not user:
            return None
        salt = AuthService.__get_salt_from_db_entry(user=user)
        if not salt:
            return None
        if AuthService.hash_password(login.password, salt) == user.password:
            return user
        return None

    @staticmethod
    def username_exists(login: LoginDto, db_context: SQLAlchemy) -> bool:
        return AuthService.__get_user_from_db(username=login.username, db_context=db_context) is not None

    @staticmethod
    def __get_salt_from_db_entry(user: UserDB) -> str:
        return user.salt

    @staticmethod
    def __get_user_from_db(username: str, db_context: SQLAlchemy) -> UserDB:
        return db_context.session.query(UserDB).filter_by(username=username).first()

    @staticmethod
    def __create_salt() -> str:
        return os.urandom(32).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Returns hashed pw"""
        return sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
