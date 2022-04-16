import pytest
from datetime import datetime
from db_management.refresh_db import repo, refresh_db
from facades.facade_anonymous import AnonymousFacade
from tables.airline_companies import AirlineCompanies
from tables.flights import Flights
from exceptions.exception_InsufficientAccessRights import InsufficientAccessRights


facade_anonymous = AnonymousFacade()
# instantiation of the airline_facade is done by executing the functions  login in facade_anonymous


@pytest.fixture(scope='function', autouse=True)   # creating the tests facade entity
def entity_airline_facade():
    airline_facade = facade_anonymous.login(username='el_al', password='elal123')
    return airline_facade


@pytest.fixture(scope='function', autouse=True)   # removing tests data from the database
def clean_test_db():
    refresh_db()


def test_get_my_flights(entity_airline_facade):
    actual = entity_airline_facade.get_my_flights()
    expected = repo.get_by_column_value(Flights, Flights.airline_company_id, 1)
    assert actual == expected


@pytest.mark.parametrize('airline, expected',
                         [(AirlineCompanies(id=1, name='El Al', country_id=1, user_id=11), True),
                          (AirlineCompanies(id=1, name='El Al', country_id=1, user_id=11), True),
                          (AirlineCompanies(id=1000, name='Test Airlines', country_id=2, user_id=1000), False)])
def test_update_airline(entity_airline_facade, airline, expected):
    actual = entity_airline_facade.update_airline(airline)
    assert actual == expected


def test_update_airline_negative_insufficient_access_rights(entity_airline_facade):
    another_airline = AirlineCompanies(id=2, name='American Airlines', country_id=2, user_id=12)
    with pytest.raises(InsufficientAccessRights):  # The attempt to update another airline
        entity_airline_facade.update_airline(another_airline)


@pytest.mark.parametrize('new_flight, expected',
                         [(Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=2,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 12, 0, 0),
                                   remaining_tickets=10), True),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=1,   # destination_country_id == origin_country_id
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                   remaining_tickets=200), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=3,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 10, 20, 0),  # The duration of flight is too short
                                   remaining_tickets=200), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=2,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 23, 0, 0),    # The duration of flight is too long
                                   remaining_tickets=10), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=2,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 12, 0, 0),
                                   remaining_tickets=10.5), False)])   # The number of remaining tickets is not integer
def test_airline_facade_add_flight(entity_airline_facade, new_flight, expected):
    actual = entity_airline_facade.add_flight(new_flight)
    if expected is True:
        flight_after_add = repo.get_by_column_value(Flights, Flights.id, new_flight.id)[0]
        assert flight_after_add.__str__() == new_flight.__str__()
    else:
        assert actual == expected


def test_airline_facade_add_flight_negative_insufficient_access_rights(entity_airline_facade):
    flight_of_another_airline = Flights(airline_company_id=2,  # The attempt to add a flight of a non-own airline
                                        origin_country_id=1,
                                        destination_country_id=2,
                                        departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                        landing_time=datetime(2022, 10, 1, 12, 0, 0),
                                        remaining_tickets=10)
    with pytest.raises(InsufficientAccessRights):
        entity_airline_facade.add_flight(flight_of_another_airline)


@pytest.mark.parametrize('flight_for_update, expected',
                         [(Flights(airline_company_id=1,
                                   origin_country_id=2,
                                   destination_country_id=3,
                                   departure_time=datetime(2022, 10, 1, 20, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 22, 0, 0),
                                   remaining_tickets=10), True),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=1,   # destination_country_id == origin_country_id
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                   remaining_tickets=200), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=3,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 10, 20, 0),  # The duration of flight is too short
                                   remaining_tickets=200), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=2,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 23, 0, 0),   # The duration of flight is too long
                                   remaining_tickets=10), False),
                          (Flights(airline_company_id=1,
                                   origin_country_id=1,
                                   destination_country_id=2,
                                   departure_time=datetime(2022, 10, 1, 10, 0, 0),
                                   landing_time=datetime(2022, 10, 1, 12, 0, 0),
                                   remaining_tickets=10.5), False)])   # The number of remaining tickets is not integer
def test_airline_facade_update_flight(entity_airline_facade, flight_for_update, expected):
    actual = entity_airline_facade.add_flight(flight_for_update)
    if expected is True:
        flight_after_update = repo.get_by_column_value(Flights, Flights.id, flight_for_update.id)[0]
        assert flight_for_update.__str__() == flight_after_update.__str__()
    else:
        assert actual == expected


def test_airline_facade_update_flight_negative_insufficient_access_rights(entity_airline_facade):
    flight_of_another_airline = Flights(id=2, airline_company_id=2,  # The attempt to update a flight of another airline
                                        origin_country_id=2,
                                        destination_country_id=3,
                                        departure_time=datetime(2022, 3, 2, 6, 0, 10),
                                        landing_time=datetime(2022, 3, 2, 10, 0, 10),
                                        remaining_tickets=10)
    with pytest.raises(InsufficientAccessRights):
        entity_airline_facade.update_flight(flight_of_another_airline)


def test_remove_flight(entity_airline_facade):
    actual = entity_airline_facade.remove_flight(1)
    assert actual is True
    assert repo.get_by_id(Flights, id_=1) is None


def test_remove_flight_negative_insufficient_access_rights(entity_airline_facade):
    with pytest.raises(InsufficientAccessRights):  # The attempt to update a flight of another airline
        entity_airline_facade.remove_flight(2)
