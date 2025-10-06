class DomainError(Exception):
    pass

class OrderAlreadyExists(DomainError):
    pass