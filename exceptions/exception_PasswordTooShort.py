from exceptions.exception_SpecificFlightSystemNotification import SpecificFlightSystemExceptions


class PasswordTooShortException(SpecificFlightSystemExceptions):

    def __init__(self, message="The password must contain at least 6 characters."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'''\nATTENTION: {SpecificFlightSystemExceptions.__str__} 
        PasswordTooShortException: {self.message}'''
