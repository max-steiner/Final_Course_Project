from exceptions.exception_SpecificFlightSystemNotification import SpecificFlightSystemExceptions


class InsufficientAccessRights(SpecificFlightSystemExceptions):
    def __init__(self, message='Your user role does not allow you to work with this data!'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'\nInsufficientAccessRights: {self.message}'
