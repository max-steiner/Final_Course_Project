class SpecificFlightSystemExceptions(Exception):
    """General exceptions class for specific exceptions in the flight control system"""

    def __init__(self, *args):
        super().__init__(*args)
        self.message = args[0] if args else None

    def __str__(self):
        return f'Flight Control System Notification'
