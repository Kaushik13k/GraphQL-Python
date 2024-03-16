class LoginDataException(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)


class SignupDataException(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)


class MuscleGroupCreationException(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)

class TokenDataException(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)


class ResetPasswordDataException(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)
