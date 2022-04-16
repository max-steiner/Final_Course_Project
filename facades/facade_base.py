from abc import ABC, abstractmethod
from datetime import datetime
from db_management.db_config import local_session
from db_management.db_repo import DbRepo
from tables.flights import Flights
from tables.airline_companies import AirlineCompanies
from tables.countries import Countries
from tables.users import Users
from exceptions.exception_UserAlreadyExists import UserAlreadyExistsException
from exceptions.exception_PasswordTooShort import PasswordTooShortException
from logger import Logger


class FacadeBase(ABC):
    repo = DbRepo(local_session)

    @abstractmethod
    def __init__(self):
        self.logger = Logger.get_instance()

    @staticmethod
    def validate_id(id_):
        if not isinstance(id_, int):
            print('\nID must be an integer.')
            return False
        elif id_ <= 0:
            print('\nID must be positive.')
            return False
        else:
            return True

    @staticmethod
    def validate_date(datetime_):
        if not isinstance(datetime_, datetime):
            print('\nIncorrect format of data entry.')
            return False
        else:
            return True

    @staticmethod
    def validate_class(obj_, cls_):
        if not isinstance(obj_, cls_):
            print(f'\nThe entered data does not match the class {cls_}.')
            return False
        else:
            return True

    def get_all_flights(self):
        all_flights = self.repo.get_all(Flights)
        self.logger.logger.info('The function  <<get_all_flight>> successfully used')
        return all_flights

    def get_flight_by_id(self, id_):
        if self.validate_id(id_):
            flight = self.repo.get_by_id(Flights, id_)
            self.logger.logger.info('The function  <<get_flight_by_id>> successfully used')
            return flight
        else:
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<get_flight_by_id>> failed. Invalid ID')
            return False

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, datetime_):
        if self.validate_id(origin_country_id) and self.validate_id(destination_country_id):
            if self.validate_date(datetime_):
                flights_by_parameters = self.repo.get_by_condition(Flights, lambda query: query.filter(
                    Flights.origin_country_id == origin_country_id,
                    Flights.destination_country_id == destination_country_id,
                    Flights.departure_time == datetime_).all())
                self.logger.logger.info('The function  <<get_flights_by_parameters>> successfully used')
                return flights_by_parameters
            else:
                print('\nPlease,enter correct data')
                self.logger.logger.error('Function <<get_flight_by_id>> failed. Invalid data')
                return False
        else:
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<get_flight_by_id>> failed. Invalid data')
            return False

    def get_all_airlines(self):
        all_airlines = self.repo.get_all(AirlineCompanies)
        self.logger.logger.info('The function  <<get_all_airlines>> successfully used')
        return all_airlines

    def get_airline_by_id(self, id_):
        if self.validate_id(id_):
            airline_by_id = self.repo.get_by_id(AirlineCompanies, id_)
            self.logger.logger.info('The function  <<get_airline_by_id>> successfully used')
            return airline_by_id
        else:
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<get_airline_by_id>> failed. Invalid data')
        return False

    def get_airline_by_parameters(self, name, country_id):
        if self.validate_id(country_id):
            airline_by_parameters = self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                AirlineCompanies.name == name,
                AirlineCompanies.country_id == country_id).all())
            self.logger.logger.info('The function  <<get_airline_by_parameters>> successfully used')
            return airline_by_parameters
        else:
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<get_airline_by_parameters>> failed. Invalid data')
            return False

    def get_all_countries(self):
        all_countries = self.repo.get_all(Countries)
        self.logger.logger.info('The function  <<get_all_countries>> successfully used')
        return all_countries

    def get_country_by_id(self, id_):
        if self.validate_id(id_):
            country_by_id = self.repo.get_by_id(Countries, id_)
            self.logger.logger.info('The function  <<get_country_by_id>> successfully used')
            return country_by_id
        else:
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<get_country_by_id>> failed. Invalid data')
            return False

    def create_user(self, user):
        self.logger.logger.debug(
            'Attempting to create a new user>>')
        if not self.validate_class(user, Users):
            print('\nPlease,enter correct data')
            self.logger.logger.error('Function <<create_user>> failed. Invalid class User')
            return False
        elif self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == user.username).all()):
            self.logger.logger.error('Function <<create_user>> failed. UserAlreadyExistsException')
            raise UserAlreadyExistsException
        elif self.repo.get_by_condition(Users, lambda query: query.filter(Users.email == user.email).all()):
            print('\nThe specified e-mail address is already registered in the system')
            self.logger.logger.error('Function <<create_user>> failed. The specified e-mail is already registered')
            return False
        elif len(user.password) < 6:
            self.logger.logger.error('Function <<create_user>> failed. PasswordTooShortException')
            raise PasswordTooShortException
        elif user.user_role not in {1, 2, 3, 4}:
            print('\nInvalid user role!')
            self.logger.logger.error('Function <<create_user>> failed. Invalid user role')
            return False
        else:
            user.id = None
            self.repo.add(user)
            print('\nNew user creation approved')
            self.logger.logger.info('The new user has been successfully created')
            return True

    def __str__(self):
        return 'Facade_Base of flight system'

    def __repr__(self):
        return 'Facade_Base of flight system'
