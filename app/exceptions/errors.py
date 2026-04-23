class ExistingProjectNameError(Exception):
    pass

class ProjectNotFoundError(Exception):
    pass

class BoardNotFoundError(Exception):
    pass

class NotProjectOwnerError(Exception):
    pass

class NotBoardProjectError(Exception):
    pass

class ExistingBoardNameError(Exception):
    pass

class InvalidCredentials(Exception):
    pass

class ExistingEmailError(Exception):
    pass
