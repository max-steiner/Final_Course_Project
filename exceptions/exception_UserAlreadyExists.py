from exceptions.exception_SpecificFlightSystemNotification import SpecificFlightSystemExceptions


class UserAlreadyExistsException(SpecificFlightSystemExceptions):

    def __init__(self, message="This user is already registered in system!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'''\nATTENTION: {SpecificFlightSystemExceptions.__str__} 
            UserAlreadyExistException: {self.message}'''
