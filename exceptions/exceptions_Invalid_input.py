class InvalidInput(Exception):
    def __init__(self, message="Invalid input provided!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidInput: {self.message}'
