class NoNotesFoundError(Exception):

    def __init__(self, message="No Notes found"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    
    def __init__(self, message="Invalid username or password"):
        self.message = message
        super().__init__(self.message)