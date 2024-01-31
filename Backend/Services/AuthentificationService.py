import os
from Backend.Model.Login.LoginDto import LoginDto
from hashlib import sha256


class AuthService:
    def create_user(self, login: LoginDto):
        raise NotImplementedError

    def verify_user(self, login: LoginDto):
        raise NotImplementedError

    def username_exists(self, username):
        raise NotImplementedError

    @staticmethod
    def __get_salt(username):
        raise NotImplementedError


    @staticmethod
    def __create_salt():
        return os.urandom(32).hex()

    @staticmethod
    def hash_password(password, salt) -> str:
        """Returns hashed pw"""
        return sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
