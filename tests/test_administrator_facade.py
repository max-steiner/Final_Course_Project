import pytest
from tables.administrators import Administrators
from facades.facade_anonymous import AnonymousFacade
from tables.airline_companies import AirlineCompanies
from tables.customers import Customers
from tables.users import Users
from db_management.refresh_db import repo, refresh_db


facade_anonymous = AnonymousFacade()
# instantiation of the facade_administrator is done by executing the functions  login in facade_anonymous


@pytest.fixture(scope='session')   # creating the tests facade entity
def entity_admin_facade():
    admin_facade = facade_anonymous.login(username='ron_michael', password='Ron123')
    return admin_facade


@pytest.fixture(scope='function', autouse=True)   # removing tests data from the database
def clean_test_db():
    refresh_db()


def test_get_all_customers(entity_admin_facade):
    assert entity_admin_facade.get_all_customers() == repo.get_all(Customers)


def test_add_administrator(entity_admin_facade):  # The successful attempt
    admin = Administrators(first_name='Test', last_name='Test', user_id=8)
    user = Users(username='Test', password='test123', email='tests@mail.com', user_role=1)
    assert entity_admin_facade.add_administrator(user, admin) is True
    administrator_after_add = repo.get_by_column_value(Administrators, Administrators.first_name, 'Test')[0]
    assert administrator_after_add.__str__() == admin.__str__()
    user_after_add_admin = repo.get_by_column_value(Users, Users.username, 'Test')[0]
    assert user_after_add_admin.__str__() == user.__str__()


def test_add_administrator_negative_exists(entity_admin_facade):   # The unsuccessful attempt
    admin = Administrators(first_name='Test', last_name='Test', user_id=8)
    user = Users(username='Test', password='test123', email='tests@mail.com', user_role=1)
    entity_admin_facade.add_administrator(user, admin)                   # the first adding of the administrator
    assert entity_admin_facade.add_administrator(admin, user) is False   # the trying to re-add the administrator


def test_add_administrator_negative_type(entity_admin_facade):  # The unsuccessful attempt
    admin = Customers(first_name='Test', last_name='Test',  # The administrator cannot be created in classic Customer
                      address='tests',
                      phone_number='123456',
                      credit_card_number='1111 2222 3333 4444',
                      user_id=3)
    user = Users(username='Test', password='test123', email='tests@mail.com', user_role=1)
    assert entity_admin_facade.add_administrator(user, admin) is False


def test_add_airline(entity_admin_facade):    # The successful attempt
    user = Users(username='test_air', password='123456', email='test_air@mail.com', user_role=2)
    airline = AirlineCompanies(name='test_air', country_id=1, user_id=user.id)
    entity_admin_facade.add_airline(user, airline)
    airline_after_add = repo.get_by_column_value(AirlineCompanies, AirlineCompanies.name, 'test_air')[0]
    assert airline_after_add.__str__() == airline.__str__()


def test_add_airline_negative_already_exists(entity_admin_facade):   # The unsuccessful attempt
    user1 = Users(username='test_air', password='123456', email='test_air@mail.com', user_role=2)
    airline1 = AirlineCompanies(name='test_air', country_id=1, user_id=user1.id)
    entity_admin_facade.add_airline(user1, airline1)                  # the first adding of the airline
    assert entity_admin_facade.add_airline(user1, airline1) is False  # the trying to re-add the airline


def test_add_airline_negative_invalid_country(entity_admin_facade):  # invalid  country ID
    user1 = Users(username='test_air', password='123456', email='test_air@mail.com', user_role=2)
    airline1 = AirlineCompanies(name='test_air', country_id=1000, user_id=user1.id)
    assert entity_admin_facade.add_airline(user1, airline1) is False


def test_add_customer(entity_admin_facade):  # The successful attempt
    user = Users(username='tests', password='test12345', email='test123@mail.com', user_role=3)
    customer = Customers(first_name='Test_name', last_name='Test_surname', address='test_address',
                         phone_number='11112222', credit_card_number='0000 0000 0000 0000', user_id=8)
    entity_admin_facade.add_customer(user, customer)
    assert repo.get_by_column_value(Customers, Customers.first_name, 'Test_name') != []
    assert repo.get_by_column_value(Users, Users.username, 'tests') != []


def test_add_customer_negative_credit_card_already_exists(entity_admin_facade):  # the same credit card number
    user1 = Users(username='test1', password='test12345', email='test123@mail.com', user_role=3)
    customer1 = Customers(first_name='Test_name1', last_name='Test_surname1', address='test_address1',
                          phone_number='0000000', credit_card_number='0000 0000 0000 0000', user_id=8)
    entity_admin_facade.add_customer(user1, customer1)
    user2 = Users(username='test2', password='test9876', email='test567@mail.com', user_role=3)
    customer2 = Customers(first_name='Test_name2', last_name='Test_surname2', address='test_address2',
                          phone_number='1111111', credit_card_number='0000 0000 0000 0000', user_id=8)
    assert entity_admin_facade.add_customer(user2, customer2) is False


def test_remove_administrator(entity_admin_facade):  # The successful attempt
    admin = Administrators(first_name='Test', last_name='Test', user_id=8)
    user = Users(username='Test', password='test123', email='tests@mail.com', user_role=1)
    entity_admin_facade.add_administrator(user, admin)
    assert entity_admin_facade.remove_administrator(admin) is True
    assert repo.get_by_column_value(Administrators, Administrators.first_name, 'Test') == []


def test_remove_administrator_negative(entity_admin_facade):   # the administrator is not registered
    admin = Administrators(first_name='Test', last_name='Test', user_id=8)
    assert entity_admin_facade.remove_administrator(admin) is False


def test_remove_airline(entity_admin_facade):  # The successful attempt
    user1 = Users(username='test_air', password='123456', email='test_air@mail.com', user_role=2)
    airline1 = AirlineCompanies(name='test_air', country_id=1, user_id=user1.id)
    entity_admin_facade.add_airline(user1, airline1)
    entity_admin_facade.remove_airline(airline1)
    assert repo.get_by_column_value(AirlineCompanies, AirlineCompanies.name, 'test_air') == []


def test_remove_airline_negative(entity_admin_facade):  # the airline is not registered
    user1 = Users(username='test_air', password='123456', email='test_air@mail.com', user_role=2)
    airline1 = AirlineCompanies(name='test_air', country_id=1, user_id=user1.id)
    entity_admin_facade.remove_airline(airline1)
    assert entity_admin_facade.remove_airline(airline1) is False


def test_remove_customer(entity_admin_facade):  # The successful attempts adding and removing the customer
    user = Users(username='tests', password='test12345', email='test123@mail.com', user_role=3)
    customer = Customers(first_name='Test_name', last_name='Test_surname', address='test_address',
                         phone_number='11112222', credit_card_number='0000 0000 0000 0000', user_id=8)
    entity_admin_facade.add_customer(user, customer)
    assert repo.get_by_column_value(Customers, Customers.first_name, 'Test_name') != []
    assert entity_admin_facade.remove_customer(customer) is True
    assert repo.get_by_column_value(Customers, Customers.first_name, 'Test_name') == []


def test_remove_customer_negative(entity_admin_facade):   # the customer is not registered
    customer = Customers(first_name='Test_name', last_name='Test_surname', address='test_address',
                         phone_number='11112222', credit_card_number='0000 0000 0000 0000', user_id=8)
    assert entity_admin_facade.remove_customer(customer) is False
