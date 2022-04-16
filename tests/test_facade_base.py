import pytest
from tables.countries import Countries
from datetime import datetime
from facades.facade_anonymous import AnonymousFacade
from tables.airline_companies import AirlineCompanies
from tables.users import Users
from tables.flights import Flights
from db_management.refresh_db import repo, refresh_db
from exceptions.exception_PasswordTooShort import PasswordTooShortException
from exceptions.exception_UserAlreadyExists import UserAlreadyExistsException


facade_anonymous = AnonymousFacade()


@pytest.fixture(scope='function', autouse=True)
def entity_facade_base():
    an_facade = facade_anonymous
    return an_facade


@pytest.fixture(scope='function', autouse=True)
def clean_test_db():
    refresh_db()


def test_get_all_flights(entity_facade_base):
    assert entity_facade_base.get_all_flights() == repo.get_all(Flights)


def test_get_flight_by_id_positive(entity_facade_base):
    assert entity_facade_base.get_flight_by_id(1) == repo.get_by_id(Flights, 1)


def test_get_flight_by_id_negative(entity_facade_base):
    assert entity_facade_base.get_flight_by_id(10000) is None


@pytest.mark.parametrize('origin_country_id, destination_country_id, datetime_, flight_id',
                         [(1, 2, datetime(2022, 3, 1, 10, 30), 1),         # the flight already exists
                          (1, 3, datetime(2022, 3, 1, 10, 30), False)])    # the flight does not exist
def test_get_flights_by_parameters_positive(entity_facade_base, origin_country_id,
                                            destination_country_id, datetime_, flight_id):
    flights_by_parameters = entity_facade_base.get_flights_by_parameters(
        origin_country_id, destination_country_id, datetime_)
    if flights_by_parameters:
        actual = flights_by_parameters[0].id
    else:
        actual = False
    expected = flight_id
    assert actual == expected


def test_get_all_airlines(entity_facade_base):
    assert entity_facade_base.get_all_airlines() == repo.get_all(AirlineCompanies)


@pytest.mark.parametrize('id_, airline_user_id',
                         [(1, 11),
                          (2, 12),
                          ('1', False),             # invalid id
                          (100, False)])            # the airline does not exist
def test_get_airline_by_id(entity_facade_base, id_, airline_user_id):
    airline = entity_facade_base.get_airline_by_id(id_)
    if airline:
        actual = airline.user_id
    else:
        actual = False
    expected = airline_user_id
    assert actual == expected


def test_get_all_countries(entity_facade_base):
    assert entity_facade_base.get_all_countries() == repo. get_all(Countries)


@pytest.mark.parametrize('id_, name',
                         [(1, 'Israel'),
                          (2, 'USA'),
                          ('1', False),             # invalid id
                          (100, False)])            # the country does not exist
def test_get_country_by_id(entity_facade_base, id_, name):
    country = entity_facade_base.get_country_by_id(id_)
    if country:
        actual = f'{country.name}'
    else:
        actual = False
    expected = name
    assert actual == expected


def test_create_user(entity_facade_base):
    user_new = Users(username='Test_name', password='123456', email='tests@mail.com', user_role=3)
    entity_facade_base.create_user(user_new)
    user_after_create = repo.get_by_column_value(Users, Users.username, 'Test_name')[0]
    assert user_after_create is not None
    assert user_after_create.__str__() == user_new.__str__()


def test_create_user_negative_exceptions(entity_facade_base):
    with pytest.raises(PasswordTooShortException):
        entity_facade_base.create_user(Users(
            username='Test_name', password='12345', email='tests@mail.com', user_role=3))  # the password < 6 characters
    entity_facade_base.create_user(Users(
        username='Test_name', password='123456', email='tests@mail.com', user_role=3))  # the user already exists
    with pytest.raises(UserAlreadyExistsException):
        entity_facade_base.create_user(Users(
            username='Test_name', password='123456', email='tests@mail.com', user_role=3))
