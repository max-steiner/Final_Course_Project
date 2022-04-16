from facades.facade_base import FacadeBase
from tables.users import Users
from facades.facade_customer import CustomerFacade
from facades.facade_administrator import AdministratorFacade
from facades.facade_airline import AirlineFacade
from tables.customers import Customers
from login_token import LoginToken
from logger import Logger


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__()
        self.logger = Logger.get_instance()

    def login(self, username, password):
        self.logger.logger.debug(f'Attempting login in system. Username: {username}')
        if not self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username).all()):
            print('\nUser with this name is not registered in the system')
            self.logger.logger.error(f'User with this name ({username}) is not registered in the system')
            return False
        elif not self.repo.get_by_condition(Users, lambda query: query.filter(Users.password == password).all()):
            print('\nInvalid password')
            self.logger.logger.error(f'Invalid password: {password} for username: {username}')
            return False
        else:
            print('\nLogin allowed')
            user = self.repo.get_by_condition(
                Users, lambda query: query.filter(Users.username == username, Users.password == password))
            if user[0].user_role == 1:
                administrator_facade = AdministratorFacade(
                    login_token=LoginToken(id_=user[0].administrators[0].id,
                                           name=user[0].username,
                                           user_role='Administrator'))
                self.logger.logger.info(f'Login allowed. Administrator: {user[0].username}')
                return administrator_facade
            elif user[0].user_role == 2:
                airline_facade = AirlineFacade(
                    login_token=LoginToken(id_=user[0].airline_companies[0].id,
                                           name=user[0].username,
                                           user_role='Airline'))
                self.logger.logger.info(f'Login allowed. Airline: {user[0].username}')
                return airline_facade
            elif user[0].user_role == 3:
                customer_facade = CustomerFacade(
                    login_token=LoginToken(id_=user[0].customers[0].id,
                                           name=user[0].username,
                                           user_role='Customer'))
                self.logger.logger.info(f'Login allowed. Customer: {user[0].username}')
                return customer_facade
            else:
                print('\nInvalid user role!')
                self.logger.logger.info(f'Invalid user role!. User: {username}')
                return False

    def add_customer(self, user, customer):
        self.logger.logger.debug(f'Attempting adding customer to system. Username: {user.username}')
        if not self.validate_class(user, Users):
            print('\nPlease,enter correct data')
            self.logger.logger.error(f'Invalid data: {user}')
            return False
        elif not self.validate_class(customer, Customers):
            self.logger.logger.error(f'Invalid data: {customer}')
            return False
        elif user.user_role != 3:
            print('\nInvalid user role!')
            self.logger.logger.error(f'Invalid user role: {user}')
            return False
        elif self.repo.get_by_condition(
                Customers, lambda query: query.filter(Customers.phone_number == customer.phone_number).all()):
            print('\nThe customer with the this phone number is already registered in the system')
            self.logger.logger.error(f'Invalid data: phone number')
            return False
        elif self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_number == customer.credit_card_number).all()):
            print('The customer with this credit card number is already registered in the system')
            self.logger.logger.error(f'Invalid data: credit card number')
            return False
        else:
            self.create_user(user)
            customer.id = None
            customer.user_id = user.id
            self.repo.add(customer)
            print('Adding a new customer approved')
            self.logger.logger.info(f'Adding a new customer {customer} approved')
            return True

    def __str__(self):
        return 'AnonymousFacade of flight system'

    def __repr__(self):
        return 'AnonymousFacade of flight system'
