from facades.facade_base import FacadeBase
from tables.customers import Customers
from tables.tickets import Tickets
from tables.flights import Flights
from exceptions.exception_TicketNotFound import TicketNotFoundException
from exceptions.exception_NoMoreTicketsForFlights import NoMoreTicketsForFlightsException
from exceptions.exception_InsufficientAccessRights import InsufficientAccessRights
from logger import Logger


class CustomerFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def update_customer(self, customer):
        self.logger.logger.debug(
            f'Attempting to update customer <<{self.login_token.id}>>')
        if not self.validate_class(customer, Customers):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<update_customer>> failed. Customer <<{self.login_token.id}>>. Invalid class Customers')
            return False
        customer_for_update = self.repo.get_by_condition(
            Customers, lambda query: query.filter(Customers.id == customer.id).all())
        if not customer_for_update:
            print('\n This customer is not registered in the system')
            self.logger.logger.error(
                f'Function <<update_customer>> failed.The customer <<{customer}>> is not registered in the system')
            return False
        if self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.phone_number == customer.phone_number).all()) and \
                self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.phone_number == customer.phone_number).all()) != customer_for_update:
            self.logger.logger.error(f'Function <<update_customer>> failed. Customer <<{self.login_token.id}>>. '
                                     f'The phone number is already exists in the system')
            return False
        if self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_number == customer.credit_card_number).all()) and \
                self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.credit_card_number == customer.credit_card_number).all()) != customer_for_update:
            self.logger.logger.error(f'Function <<update_customer>> failed. Customer <<{self.login_token.id}>>. '
                                     f'The credit_card_number is already exists in the system')
            return False
        customer_check = self.repo.get_by_id(Customers, customer.id)
        if self.login_token.id != customer_check.id:
            self.logger.logger.error(
                f'InsufficientAccessRights for updating customer {customer_check}')
            raise InsufficientAccessRights
        self.repo.update_by_id(Customers, Customers.id, self.login_token.id,
                               {Customers.first_name: customer.first_name, Customers.last_name: customer.last_name,
                                Customers.address: customer.address, Customers.phone_number: customer.phone_number,
                                Customers.credit_card_number: customer.credit_card_number})
        print('\nInformation about the customer has been successfully updated')
        self.logger.logger.info(f'The customer with ID<<{customer_for_update}>> updated')
        return True

    def add_ticket(self, ticket):
        self.logger.logger.debug(
            f'Attempting to add ticket. Customer <<{self.login_token.id}>>')
        flight = self.get_flight_by_id(ticket.flight_id)
        if not self.validate_class(ticket, Tickets):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<add_ticket>> failed. Customer <<{self.login_token.id}>>. Invalid class Tickets')
            return False
        elif self.repo.get_by_condition(
                Tickets, lambda query: query.filter(Tickets.id == ticket.id).all()):
            print('\nTicket with this ID is already registered in the system')
            self.logger.logger.error(
                f'Function <<add_ticket>> failed. Customer <<{self.login_token.id}>>. The ticket is already registered')
            return False
        elif not self.repo.get_by_condition(
                Flights, lambda query: query.filter(Flights.id == ticket.flight_id).all()):
            print('\nFlight ID is incorrect')
            self.logger.logger.error(
                f'Function <<add_ticket>> failed. Customer <<{self.login_token.id}>>. Flight ID is incorrect')
            return False
        elif flight.remaining_tickets <= 0:
            self.logger.logger.error(
                f'Function <<add_ticket>> failed. Customer <<{self.login_token.id}>>. NoMoreTicketsForFlightsException')
            raise NoMoreTicketsForFlightsException
        else:
            customer_check = self.repo.get_by_id(Customers, ticket.customer_id)
            if self.login_token.id != customer_check.id:
                self.logger.logger.error(
                    f'InsufficientAccessRights for adding ticket by customer {self.login_token.id}')
                raise InsufficientAccessRights
            else:
                ticket.id = None
                self.repo.add(ticket)
                self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                       {'remaining_tickets': flight.remaining_tickets - 1})
                print('\nNew ticket addition approved')
                self.logger.logger.info(
                    f'The customer with ID<<{self.login_token.id}>> added new ticket with ID <<{ticket.id}>>')
                return True

    def remove_ticket(self, ticket):
        self.logger.logger.debug(
            f'Attempting to remove ticket <<{ticket}>>. Customer <<{self.login_token.id}>>')
        flight = self.get_flight_by_id(ticket.flight_id)
        if not self.validate_class(ticket, Tickets):
            print('\nPlease,enter correct data')
            self.logger.logger.error(
                f'Function <<remove_ticket>> failed. Customer <<{self.login_token.id}>>. Invalid class Tickets')
            return False
        elif not self.repo.get_by_condition(
                Tickets, lambda query: query.filter(Tickets.id == ticket.id).all()):
            self.logger.logger.error(
                f'Function <<remove_ticket>> failed. Customer <<{self.login_token.id}>>. TicketNotFoundException')
            raise TicketNotFoundException
        elif not self.repo.get_by_condition(
                Tickets, lambda query: query.filter(Tickets.flight_id == ticket.flight_id).all()):
            print('\nFlight ID is incorrect')
            self.logger.logger.error(
                f'Function <<add_ticket>> failed. Customer <<{self.login_token.id}>>. Flight ID is incorrect')
            return False
        else:
            customer_check = self.repo.get_by_id(Customers, ticket.customer_id)
            if self.login_token.id != customer_check.id:
                self.logger.logger.error(
                    f'InsufficientAccessRights for removing ticket by customer {self.login_token.id}')
                raise InsufficientAccessRights
            else:
                removed_ticket_id = ticket.id
                self.repo.delete_by_id(Tickets, Tickets.id, ticket.id)
                print('\nThe ticket removed successfully')
                self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                       {'remaining_tickets': flight.remaining_tickets + 1})
                self.logger.logger.info(
                    f'The  customer with ID<<{self.login_token.id}>> removed ticket <<{removed_ticket_id}>>')
                return True

    def get_my_tickets(self):
        my_tickets = self.repo.get_by_condition(Tickets, lambda query: query.filter(
            Tickets.customer_id == self.login_token.id)).all()
        self.logger.logger.info(
            f'The  customer with ID<<{self.login_token.id}>> used the function get_my_ticket')
        return my_tickets

    def __str__(self):
        return '\nCustomer facade_Base of flight system'

    def __repr__(self):
        return '\nCustomer facade_Base of flight system'
