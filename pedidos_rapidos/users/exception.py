class UserAlreadyCreatedException(Exception):
    def __init__(self, message):
        self.msg = message

class PasswordDontMatchException(Exception):
    def __init__(self, message):
        self.msg = message

