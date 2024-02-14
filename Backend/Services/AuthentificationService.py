import os
from Backend.Model.Login.LoginDto import LoginDto
from hashlib import sha256
from Backend._DatabaseCall import UserDB


class AuthService:
    @staticmethod
    def create_user(login: LoginDto):
        if AuthService.username_exists(login):
            return None
        salt = AuthService.__create_salt()
        password = AuthService.hash_password(login.password, salt)
        user = UserDB(username=login.username, password=password, salt=salt)
        user.save()
        return user

    @staticmethod
    def verify_user(login: LoginDto):
        user = AuthService.__get_user_from_db(login.username)
        if not user:
            return None
        salt = AuthService.__get_salt_from_db_entry(login.username)
        if not salt:
            return None
        if AuthService.hash_password(login.password, salt) == user.password:
            return user
        return None

    @staticmethod
    def username_exists(login: LoginDto) -> bool:
        return AuthService.__get_user_from_db(login.username) is not None

    @staticmethod
    def __get_salt_from_db_entry(user: UserDB) -> str:
        return user.salt

    @staticmethod
    def __get_user_from_db(username: str) -> UserDB:
        return UserDB.query.filter_by(username=username).first()

    @staticmethod
    def __create_salt() -> str:
        return os.urandom(32).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Returns hashed pw"""
        return sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
