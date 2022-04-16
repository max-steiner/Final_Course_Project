from exceptions.exception_SpecificFlightSystemNotification import SpecificFlightSystemExceptions


class NoMoreTicketsForFlightsException(SpecificFlightSystemExceptions):

    def __init__(self, message="There are no available tickets for this flight."):
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f'''\nATTENTION: {SpecificFlightSystemExceptions.__str__} 
        NoMoreTicketsForFlightsException {self.message}'''
