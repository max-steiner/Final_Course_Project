from exceptions.exception_SpecificFlightSystemNotification import SpecificFlightSystemExceptions


class TicketNotFoundException(SpecificFlightSystemExceptions):
    """When trying to remove a ticket with ID that does not exist"""

    def __init__(self, message="The ticket with the specified data is not registered in the system."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'''\nATTENTION: {SpecificFlightSystemExceptions.__str__} 
        TicketNotFoundException: {self.message}'''
