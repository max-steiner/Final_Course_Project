from facades.facade_base import FacadeBase
from tables.customers import Customers
from tables.airline_companies import AirlineCompanies
from tables.administrators import Administrators
from tables.countries import Countries
from tables.users import Users
from logger import Logger


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def get_all_customers(self):
        self.logger.logger.debug(
            f'Attempting to used the function <<get_all_customer>> by administrator <<{self.login_token.id}>>')
        all_customers = self.repo.get_all(Customers)
        self.logger.logger.info(
            f'The administrator <<{self.login_token.id}>> successfully used the function <<get_all_customer>>')
        return all_customers

    def add_airline(self, user, airline):
        self.logger.logger.debug(
            f'Attempting to used the function <<add_airline>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(airline, AirlineCompanies):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<add_airline>> failed. Admin <<{self.login_token.id}>>. Invalid class Airline')
            return False
        elif self.repo.get_by_condition(
                AirlineCompanies, lambda query: query.filter(AirlineCompanies.id == airline.id).all()):
            print('\nThis airline company is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_airline>> failed. Admin <<{self.login_token.id}>>. The airline is already registered')
            return False
        elif self.repo.get_by_condition(
                AirlineCompanies, lambda query: query.filter(AirlineCompanies.name == airline.name).all()):
            print('\nThe airline company with the this name is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_airline>> failed. Admin <<{self.login_token.id}>>. Invalid airline name')
            return False
        elif not self.repo.get_by_condition(
                Countries, lambda query: query.filter(Countries.id == airline.country_id).all()):
            print('\nThe specified country is not registered in the system')
            self.logger.logger.error(
                f'Function <<add_airline>> failed. Admin <<{self.login_token.id}>>. Invalid country')
            return False
        else:
            user.user_role = 2
            user.id = None
            self.create_user(user)
            airline.id = None
            self.repo.add(airline)
            print('\nAdding a new airline approved')
            self.logger.logger.info(
                f'Adding a new airline approved <<{airline.name}. Admin <<{self.login_token.id}>>')
            return True

    def add_customer(self, user, customer):
        self.logger.logger.debug(
            f'Attempting to used the function <<add_customer>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(user, Users):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid class Users')
            return False
        elif not self.validate_class(customer, Customers):
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid class Customers')
            return False
        elif self.repo.get_by_condition(
                Customers, lambda query: query.filter(Customers.phone_number == customer.phone_number).all()):
            print('\nThe customer with the this phone number is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid user role')
            return False
        elif self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_number == customer.credit_card_number).all()):
            print('\nThe customer with this credit card number is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid credit card number')
            return False
        else:
            user.user_role = 3
            user.id = None
            self.create_user(user)
            customer.id = None
            self.repo.add(customer)
            print('\nAdding a new customer approved')
            self.logger.logger.info(
                f'Adding a new customer approved <<{customer.id}>>. Admin <<{self.login_token.id}>>')
            return True

    def add_administrator(self, user, administrator):
        self.logger.logger.debug(
            f'Attempting to used the function <<add_administrator>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(user, Users):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<add_administrator>> failed. Admin <<{self.login_token.id}>>. Invalid class Users')
            return False
        if not self.validate_class(administrator, Administrators):
            self.logger.logger.error(
                f'Function <<add_administrator>> failed. Admin <<{self.login_token.id}>>. Invalid class Administrators')
            return False
        elif self.repo.get_by_condition(
                Administrators, lambda query: query.filter(
                    Administrators.first_name == administrator.first_name).all()):
            print('\nThe administrator with the this first name is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_administrator>> failed. Admin <<{self.login_token.id}>>.'
                f' The administrator with the this first name is already registered in the system')
        elif self.repo.get_by_condition(
            Administrators, lambda query: query.filter(
                Administrators.last_name == administrator.last_name).all()):
            print('\nThe administrator with the this last name is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_administrator>> failed. Admin <<{self.login_token.id}>>.'
                f' The administrator with the this last name is already registered in the system')
            return False
        else:
            user.user_role = 1
            user.id = None
            self.create_user(user)
            administrator.id = None
            self.repo.add(administrator)
            print('\nAdding a new administrator approved')
            self.logger.logger.info(
                f'Adding a new administrator approved <<{administrator.id}>>. Admin <<{self.login_token.id}>>')
            return True

    def remove_airline(self, airline):
        self.logger.logger.debug(
            f'Attempting to used the function <<remove_airline>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(airline, AirlineCompanies):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<remove_airline>> failed. Admin <<{self.login_token.id}>>. Invalid class AirlineCompanies')
            return False
        if not self.repo.get_by_condition(
                AirlineCompanies, lambda query: query.filter(AirlineCompanies.name == airline.name).all()):
            print('\nAirline with this name is not registered in the system')
            self.logger.logger.error(
                f'Function <<remove_airline>> failed. Admin <<{self.login_token.id}>>. Airline is not registered')
            return False
        else:
            remove_airline_id = airline.id
            self.repo.delete_by_id(AirlineCompanies, AirlineCompanies.id, airline.id)
            print('\nAirline information has been successfully removed')
            self.logger.logger.info(
                f'Removing airline <<{remove_airline_id}>> approved. Admin <<{self.login_token.id}>>')
            return True

    def remove_customer(self, customer):
        self.logger.logger.debug(
            f'Attempting to used the function <<remove_customer>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(customer, Customers):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<remove_customer>> failed. Admin <<{self.login_token.id}>>. Invalid class Customer')
            return False
        if not self.repo.get_by_condition(
                Customers, lambda query: query.filter(Customers.id == customer.id).all()):
            print('\nThis customer is not registered in the system')
            self.logger.logger.error(
                f'Function <<remove_customer>> failed. Admin <<{self.login_token.id}>>. The customer is not registered')
            return False
        else:
            remove_customer_id = customer.id
            self.repo.delete_by_id(Customers, Customers.id, customer.id)
            print('\nInformation about customer has been successfully removed')
            self.logger.logger.info(
                f'Removing customer <<{remove_customer_id}>> approved. Admin <<{self.login_token.id}>>')
            return True

    def remove_administrator(self, administrator):
        self.logger.logger.debug(
            f'Attempting to used the function <<remove_administrator>> by administrator <<{self.login_token.id}>>')
        if not self.validate_class(administrator, Administrators):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<remove_administrator>> failed. Admin <<{self.login_token.id}>>. '
                f'Invalid class Administrators')
            return False
        if not self.repo.get_by_condition(
                Administrators, lambda query: query.filter(
                    Administrators.first_name == administrator.first_name).all()):
            print('\nAdministrator with this first name is not registered in the system')
            self.logger.logger.error(
                f'Function <<remove_administrator>> failed. Admin <<{self.login_token.id}>>. '
                f'Administrator with this first name is not registered in the system')
            return False
        else:
            remove_admin_id = administrator.id
            self.repo.delete_by_id(Administrators, Administrators.id, administrator.id)
            print('\nInformation about the administrator has been successfully removed')
            self.logger.logger.info(
                f'Removing administrator <<{remove_admin_id}>> approved. Admin <<{self.login_token.id}>>')
            return True

    def __str__(self):
        return '\nAdministratorFacade of flight system'

    def __repr__(self):
        return '\nAdministratorFacade of flight system'
