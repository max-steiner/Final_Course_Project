import pytest
from facades.facade_anonymous import AnonymousFacade
from db_management.refresh_db import repo, refresh_db
from tables.tickets import Tickets
from tables.customers import Customers
from exceptions.exception_TicketNotFound import TicketNotFoundException
from exceptions.exception_InsufficientAccessRights import InsufficientAccessRights
from exceptions.exception_NoMoreTicketsForFlights import NoMoreTicketsForFlightsException


facade_anonymous = AnonymousFacade()
# instantiation of the customer_facade is done by executing the functions  login in facade_anonymous


@pytest.fixture(scope='function', autouse=True)   # creating the tests facade entity
def entity_customer_facade():
    customer_facade = facade_anonymous.login(username='meyer_steiner', password='Meyer123')
    return customer_facade


@pytest.fixture(scope='function', autouse=True)   # removing tests data from the database
def clean_test_db():
    refresh_db()


@pytest.mark.parametrize('customer, expected',
                         [(Customers(id=1, first_name='Meyer', last_name='Steiner',
                                     address='Test',
                                     phone_number='054-972-00-28',
                                     credit_card_number='1234 5679 2345 6789',
                                     user_id=3), True),
                          (Customers(id=1, first_name='Meyer', last_name='Steiner',
                                     address='Test',
                                     phone_number='tests',
                                     credit_card_number='1234 5679 2345 6789',
                                     user_id=3), True),
                          (Customers(id=1, first_name='Meyer', last_name='Steiner',
                                     address='Test',
                                     phone_number='054-972-00-28',
                                     credit_card_number='tests',
                                     user_id=3), True),
                          (Customers(id=1000, first_name='Test_name', last_name='Test_surname',
                                     address='Test',
                                     phone_number='0000000',
                                     credit_card_number='12345',
                                     user_id=3), False)])  # the customer does not exist
def test_customer_facade_update_customer(entity_customer_facade, customer, expected):
    actual = entity_customer_facade.update_customer(customer)
    if expected is True:
        customer_after_update = repo.get_by_column_value(Customers, Customers.id, customer.id)[0]
        assert customer.__str__() == customer_after_update.__str__()
    else:
        assert actual == expected


def test_customer_facade_update_customer_negative_insufficient_access_rights(entity_customer_facade):
    another_customer = Customers(id=4, first_name='Mark', last_name='Dayan',
                                 address='Israel, Haifa, st. Rotshild 14/22',
                                 phone_number='052-485-18-18',
                                 credit_card_number='4563 4123 8765 5436',
                                 user_id=6)
    with pytest.raises(InsufficientAccessRights):     # the attempt to update another customer
        entity_customer_facade.update_customer(another_customer)


def test_get_my_tickets(entity_customer_facade):
    assert entity_customer_facade.get_my_tickets() == repo.get_by_column_value(Tickets, Tickets.customer_id, 1)


def test_remove_ticket(entity_customer_facade):
    ticket_for_remove = Tickets(id=1, flight_id=1, customer_id=1)
    assert entity_customer_facade.remove_ticket(ticket_for_remove) is True
    assert repo.get_by_id(Tickets, 1) is None


def test_remove_ticket_negative_ticket_not_registered(entity_customer_facade):
    ticket_for_remove = Tickets(id=1000, flight_id=1, customer_id=1)    # the ticket is not registered
    with pytest.raises(TicketNotFoundException):
        entity_customer_facade.remove_ticket(ticket_for_remove)


def test_remove_ticket_negative_insufficient_access_rights(entity_customer_facade):
    ticket_for_remove = Tickets(id=2, flight_id=1, customer_id=2)    # the attempt to delete a non-owned ticket
    with pytest.raises(InsufficientAccessRights):
        entity_customer_facade.remove_ticket(ticket_for_remove)


def test_add_ticket(entity_customer_facade):
    ticket_new = Tickets(id=999, flight_id=3, customer_id=1)
    assert entity_customer_facade.add_ticket(ticket_new) is True
    assert repo.get_by_column_value(Tickets, Tickets.id, ticket_new.id)[0].__str__() == ticket_new.__str__()


def test_add_ticket_no_more_tickets(entity_customer_facade):
    ticket_new = Tickets(id=1000, flight_id=4, customer_id=1)  # there are no tickets for this flight
    with pytest.raises(NoMoreTicketsForFlightsException):
        entity_customer_facade.add_ticket(ticket_new)


def test_add_ticket_insufficient_access_rights(entity_customer_facade):
    ticket_new = Tickets(id=1000, flight_id=1, customer_id=2)  # attempt to add a ticket to another customer
    with pytest.raises(InsufficientAccessRights):
        entity_customer_facade.add_ticket(ticket_new)
