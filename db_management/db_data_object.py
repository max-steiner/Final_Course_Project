from db_management.db_data_gen import DbDataGen
from exceptions.exceptions_Invalid_input import InvalidInput


class DbDataObject:

    def __init__(self, customers, airlines, flights_per_company, tickets_per_customer):
        self.customers = customers
        self.airlines = airlines
        self.flights_per_company = flights_per_company
        self.tickets_per_customer = tickets_per_customer
        self.db_gen = DbDataGen()

    def validate(self):
        if not isinstance(self.customers, int) or \
                not isinstance(self.airlines, int) or \
                not isinstance(self.flights_per_company, int) or \
                not isinstance(self.tickets_per_customer, int) or \
                self.airlines < 1 or \
                self.customers < 1 or \
                self.flights_per_company < 1 or \
                self.tickets_per_customer < 1 or \
                self.airlines > 150 or \
                (self.airlines * self.flights_per_company) < self.tickets_per_customer: raise InvalidInput

    def generate(self):
        self.db_gen.generate_admin()
        self.db_gen.generate_airline_companies(self.airlines)
        self.db_gen.generate_customers(self.customers)
        self.db_gen.generate_flights_per_company(self.flights_per_company)
        self.db_gen.generate_tickets_per_customer(self.tickets_per_customer)

    def __dict__(self):
        return {'customers': self.customers,
                'airlines': self.airlines,
                'flights_per_company': self.flights_per_company,
                'tickets_per_customer': self.tickets_per_customer}

    def __str__(self):
        return f'   {{customers: {self.customers}\n\
                    airlines: {self.airlines}\n\
                    flights_per_airline: {self.flights_per_company}\n\
                    tickets_per_customer: {self.tickets_per_customer}}}'


