import pytest
from facades.facade_anonymous import AnonymousFacade
from facades.facade_administrator import AdministratorFacade
from facades.facade_customer import CustomerFacade
from facades.facade_airline import AirlineFacade
from tables.customers import Customers
from tables.users import Users
from db_management.refresh_db import refresh_db, repo


@pytest.fixture(scope='function', autouse=True)  # creating the tests facade entity
def entity_anonymous_facade():
    return AnonymousFacade()


@pytest.fixture(scope='function', autouse=True)    # removing tests data from the database
def clean_test_db():
    refresh_db()


@pytest.mark.parametrize('username, password, expected',
                         [('ron_michael', 'Ron123', AdministratorFacade),
                          ('ron_michael', 'Ron567', False),      # Invalid password
                          ('rami_shaul', 'Rami123', AdministratorFacade),
                          ('rami_shaul', 'Rami567', False),      # Invalid password
                          ('el_al', 'elal123', AirlineFacade),
                          ('meyer_steiner', 'Meyer123', CustomerFacade),
                          ('meyer_steiner', 'Meyer12', False),   # Invalid password
                          ('mahmud_abbas', 'Mahmud123', CustomerFacade),
                          ('abbas_mahmud', 'Mahmud123', False),  # Invalid name
                          ('12345', 'liam 123', False),          # Invalid name
                          ('name_user', 'pass123', False)])   # User is not registered in the system
def test_anonymous_facade_login(entity_anonymous_facade, username, password, expected):
    actual = entity_anonymous_facade.login(username, password)
    if expected is False:
        assert actual == expected
    else:
        assert isinstance(actual, expected)


@pytest.mark.parametrize('user_new, customer_new, expected',
                         [(Users(username='test_user',
                                 password='123456',
                                 email='test_address@mail.com',
                                 user_role=3),
                           Customers(first_name='Test_name',   # The successful attempt
                                     last_name='Test_surname',
                                     address='Test_address',
                                     phone_number='1234567789',
                                     credit_card_number='1111 2222 3333 2222 3333'), True),
                          (Users(username='test_user',
                                 password='123456',
                                 email='test_address@mail.com',
                                 user_role=3),
                           Customers(first_name='Test_name',   # The phone number is already exists
                                     last_name='Test_surname',
                                     address='Test_address',
                                     phone_number='054-972-00-28',
                                     credit_card_number='1111 2222 3333 2222 3333'), False),
                          (Users(username='test_user',
                                 password='123456',
                                 email='test_address@mail.com',
                                 user_role=3),
                           Customers(first_name='Test_name',   # The credit card number is already exists
                                     last_name='Test_surname',
                                     address='Test_address',
                                     phone_number='1234567789',
                                     credit_card_number='9586 5349 545 3439'), False),
                          (Users(username='test_user',         # Invalid user role
                                 password='123456',
                                 email='test_address@mail.com',
                                 user_role=2),
                           Customers(first_name='Test_name',
                                     last_name='Test_surname',
                                     address='Test_address',
                                     phone_number='1234567789',
                                     credit_card_number='1111 2222 3333 2222 3333'), False)])
def test_anonymous_facade_add_customer(entity_anonymous_facade, user_new, customer_new, expected):
    actual = entity_anonymous_facade.add_customer(user_new, customer_new)
    if expected is True:
        customer_after_add = repo.get_by_column_value(Customers, Customers.id, customer_new.id)[0]
        assert customer_after_add.__str__() == customer_new.__str__()
        user_new_after_add_customer = repo.get_by_column_value(Users, Users.id, customer_new.user_id)[0]
        assert user_new_after_add_customer.__str__() == user_new.__str__()
    else:
        assert actual == expected
