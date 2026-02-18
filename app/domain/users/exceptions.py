"""Domain exceptions — represent business rule violations."""


class UserNotFoundError(Exception):
    pass


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass
