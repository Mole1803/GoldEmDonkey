from Backend.Model.Login.LoginDto import LoginDto


class LoginParser:
    usernameKey = "username"
    passwordKey = "password"

    @staticmethod
    def parse_from_request(request) -> LoginDto:
        login = LoginDto()
        login.username = request.json.get(LoginParser.usernameKey, None)
        login.password = request.json.get(LoginParser.passwordKey, None)
        return login
