from facades.facade_base import FacadeBase
from tables.flights import Flights
from tables.airline_companies import AirlineCompanies
from tables.countries import Countries
from datetime import timedelta
from exceptions.exception_InsufficientAccessRights import InsufficientAccessRights
from logger import Logger


class AirlineFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def get_my_flights(self):
        self.logger.logger.info(
            f'The airline ID <<{self.login_token.id}>> successfully used the function <get_my_flights>')
        return self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.airline_company_id == self.login_token.id).all())

    def update_airline(self, airline):
        self.logger.logger.debug(
            f'Attempting to use the function <<update_airline>> by airline with ID <<{self.login_token.id}>>')
        if not self.validate_class(airline, AirlineCompanies):
            print('Please,enter correct data')
            self.logger.logger.error(
                f'Function <<update_airline>> failed. Airline <<{self.login_token.id}>>. Invalid class Airline')
            return False
        elif not self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                AirlineCompanies.id == airline.id).all()):
            print('\nThe specified airline company is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_airline>> failed. Airline: {airline.id} is not registered in the system')
            return False
        elif not self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                AirlineCompanies.name == airline.name).all()) and \
                self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                    AirlineCompanies.name == airline.name).all()) != airline:
            print('\nThe airline company with this name is already registered in the system')
            self.logger.logger.error(
                f'Function <<update_airline>> failed. '
                f'The airline company with this name <<{airline.name}>> is already registered in the system')
            return False
        elif not self.repo.get_by_condition(Countries, lambda query: query.filter(
                Countries.id == airline.country_id).all()):
            print('\nThe specified country is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_airline>> failed. Airline: {self.login_token.id}. Invalid country')
            return False
        elif not self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                AirlineCompanies.user_id == airline.user_id).all()):
            print('\nThe specified users ID is is indicated incorrectly')
            self.logger.logger.error(
                f'Function <<update_airline>> failed. Airline: {self.login_token.id}. Invalid user ID')
            return False
        else:
            airline_check = self.repo.get_by_id(AirlineCompanies, airline.id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.info(
                    f'InsufficientAccessRights for updating airline {airline_check}. '
                    f'The attempt to update another airline')
                raise InsufficientAccessRights
            else:
                self.repo.update_by_id(AirlineCompanies, AirlineCompanies.id, self.login_token.id,
                                       {AirlineCompanies.name: airline.name,
                                        AirlineCompanies.country_id: airline.country_id})
                print('\nAirline has been successfully added')
                self.logger.logger.info(
                    f'The airline with ID<<{airline_check.id}>> has been updated')
                return True

    def add_flight(self, flight):
        self.logger.logger.debug(
            f'Attempting to use the function <<add_flight>> by airline with ID <<{self.login_token.id}>>')
        if not self.validate_class(flight, Flights):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid class Flight')
            return False
        elif self.repo.get_by_condition(Flights, lambda query: query.filter(
                Flights.id == flight.id).all()):
            print('\nThe flight with specified ID is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. The flight is already registered')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                AirlineCompanies.id == flight.airline_company_id).all()):
            print('\nThe specified airline is not registered in the system')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid airline')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                Countries.id == flight.origin_country_id).all()):
            print('\nThe specified origin country is not registered in the system')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid origin country')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            print('\nThe specified destination country is not registered in the system')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid destination country')
            return False
        elif flight.destination_country_id == flight.origin_country_id:
            print('\nAirport of departure or destination airport is indicated incorrectly')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid airports: '
                f'destination_country_id == origin_country_id')
            return False
        elif flight.departure_time > flight.landing_time or \
                (flight.landing_time - flight.departure_time) < timedelta(hours=1):
            print('\nThe flight duration is less than 1 hour')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>.'
                f'The flight duration is less than 1 hour')
            return False
        elif flight.landing_time - flight.departure_time > timedelta(hours=12):
            print('\nThe flight duration is more than 12 hour')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. '
                f'The flight duration is more than 12 hour')
            return False
        elif not isinstance(flight.remaining_tickets, int) or 300 < flight.remaining_tickets < 0:
            print('\nIncorrect information about the number of remaining tickets')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. Invalid remaining tickets data')
            return False
        else:
            airline_check = self.repo.get_by_id(AirlineCompanies, flight.airline_company_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.info(
                    f'InsufficientAccessRights for adding flight by {airline_check}. '
                    f'The attempt to add a flight for another airline')
                raise InsufficientAccessRights
            else:
                flight.id = None
                flight.airline_company_id = self.login_token.id
                self.repo.add(flight)
                print('\nThe flight added successfully')
                self.logger.logger.info(
                    f'The flight with ID<<{flight.id}>> has been added')
                return True

    def update_flight(self, flight):
        self.logger.logger.debug(
            f'Attempting to use the function <<update_flight>> by airline with ID <<{self.login_token.id}>>')
        if not self.validate_class(flight, Flights):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid class Flight')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                Flights.id == flight.id).all()):
            print('\nThe flight with specified ID is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. The flight is not registered')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                AirlineCompanies.id == flight.airline_company_id).all()):
            print('\nThe specified airline is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid airline')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                Countries.id == flight.origin_country_id).all()):
            print('\nThe specified origin country is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid origin country')
            return False
        elif not self.repo.get_by_condition(Flights, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            print('\nThe specified destination country is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid destination country')
            return False
        elif flight.destination_country_id == flight.origin_country_id:
            print('\nAirport of departure or destination airport is indicated incorrectly')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid airports: '
                f'destination_country_id == origin_country_id')
            return False
        elif flight.departure_time > flight.landing_time or \
             (flight.landing_time - flight.departure_time) < timedelta(hours=1):
            print('\nThe flight duration is less than 1 hour')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>.'
                f'The flight duration is less than 1 hour')
            return False
        elif flight.landing_time - flight.departure_time > timedelta(hours=12):
            print('\nThe flight duration is more than 12 hour')
            self.logger.logger.error(
                f'Function <<add_flight>> failed. Airline <<{self.login_token.id}>>. '
                f'The flight duration is more than 12 hour')
        elif not isinstance(flight.remaining_tickets, int) or 300 < flight.remaining_tickets < 0:
            print('\nIncorrect information about the number of remaining tickets')
            self.logger.logger.error(
                f'Function <<update_flight>> failed. Airline <<{self.login_token.id}>>. Invalid remaining tickets data')
            return False
        else:
            airline_check = self.repo.get_by_id(AirlineCompanies, flight.airline_company_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.info(
                    f'InsufficientAccessRights for updating flight {airline_check}. '
                    f'The attempt to update flight of another airline')
                raise InsufficientAccessRights
            else:
                self.repo.update_by_id(Flights, Flights.id, flight.id,
                                       {Flights.origin_country_id: flight.origin_country_id,
                                        Flights.destination_country_id: flight.destination_country_id,
                                        Flights.departure_time: flight.departure_time,
                                        Flights.landing_time: flight.landing_time,
                                        Flights.remaining_tickets: flight.remaining_tickets})
                print('Flights information has been successfully updated')
                self.logger.logger.info(
                    f'The flight with ID<<{flight.id}>> has been updated')
                return True

    def remove_flight(self, flight_id):
        self.logger.logger.debug(
            f'Attempting to use the function <<remove_flight>> by airline with ID <<{self.login_token.id}>>')
        if not self.validate_id(flight_id):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<remove_flight>> failed. Airline <<{self.login_token.id}>>. Invalid class Flight')
            return False
        flight_remove = self.repo.get_by_condition(Flights, lambda query: query.filter(
                Flights.id == flight_id).all())
        if not flight_remove:
            print('\nThe flight with the specified ID is not registered in the system')
            self.logger.logger.error(
                f'Function <<remove_flight>> failed. Airline <<{self.login_token.id}>>. The flight is not registered ')
            return False
        else:
            airline_check = self.repo.get_by_id(AirlineCompanies, flight_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.info(
                    f'InsufficientAccessRights for removing flight {airline_check}. '
                    f'The attempt to remove the flight of another airline')
                raise InsufficientAccessRights
            else:
                self.repo.delete_by_id(Flights, Flights.id, flight_id)
                print('\nThe information about the specified flight was successfully removed')
                self.logger.logger.info(
                    f'The flight with ID<<{flight_id}>> has been removed')
                return True

    def __str__(self):
        return '\nAirlineFacade of flight system'

    def __repr__(self):
        return '\nAirlineFacade of flight system'
