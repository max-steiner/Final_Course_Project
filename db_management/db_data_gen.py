import random
import httpx
import json
import trio
from faker import Faker
from datetime import timedelta
from db_management.db_config import config
from db_management.db_data_gen_base import BaseDbDataGen
from tables.users import Users
from tables.flights import Flights
from tables.tickets import Tickets
from tables.customers import Customers
from tables.administrators import Administrators
from tables.airline_companies import AirlineCompanies
from werkzeug.security import generate_password_hash


class DbDataGen(BaseDbDataGen):

    number_of_countries_in_db = int(config['limits']['max_countries_in_db'])
    max_hours_delta_t = int(config['limits']['max_hours_delta'])
    remaining_tickets_per_flight = int(config['limits']['max_tickets'])

    def __init__(self):
        super().__init__()
        self.response = config['db']['api']
        self.fake = Faker()

    async def get_data(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.response)
            return r.json()

    @staticmethod
    def generate_ccn():  # ccn - credit card number
        ccn = str(random.randint(0, 9))
        for i in range(11): ccn = ccn + str(random.randint(0, 9))
        return ccn

    @staticmethod
    def get_user_data(j_son):
        username =  j_son['results'][0]['login']['username']
        password =  j_son['results'][0]['login']['password']
        email =     j_son['results'][0]['email']
        return username, password, email

    @staticmethod
    def get_customer_data(j_son):
        first_name =    j_son['results'][0]['name']['first'],
        last_name =     j_son['results'][0]['name']['last'],
        address =       str(j_son['results'][0]['location']['street']['number']) + " " + \
                        j_son['results'][0]['location']['street']['name'] + \
                        j_son['results'][0]['location']['state'] + \
                        j_son['results'][0]['location']['country']
        phone_number =  str(j_son['results'][0]['phone'])
        return first_name, last_name, address, phone_number

    def create_user(self, j_son, user_role):
        username, password, email = self.get_user_data(j_son)
        inserted_user = Users(  username=username,
                                password=generate_password_hash(password),
                                email=email,
                                user_role=user_role)
        self.repo.add(inserted_user)
        return inserted_user

    def generate_admin(self):
        data = trio.run(self.get_data)
        user = self.create_user(data, config['user_roles']['admin'])
        self.repo.add(Administrators(first_name=data['results'][0]['name']['first'],
                                     last_name=data['results'][0]['name']['last'],
                                     user_id=user.id))

    def generate_customers(self, num):
        for i in range(num):
            data = trio.run(self.get_data)
            user = self.create_user(data, config['user_roles']['customer'])
            first_name, last_name, address, phone_number = self.get_customer_data(data)
            new_customer = Customers(first_name=first_name,
                                     last_name=last_name,
                                     address=address,
                                     phone_number=phone_number,
                                     credit_card_number=self.generate_ccn(),
                                     user_id=user.id)
            self.repo.add(new_customer)

    def generate_airline_companies(self, num):
        with open(config['db']['airlines_json']) as f: airlines = json.load(f)
        for i in range(num):
            data = trio.run(self.get_data)
            user = self.create_user(data, config['user_roles']['airline'])
            new_airline = AirlineCompanies( name=airlines[i]["name"],
                                            country_id=random.randint(1, self.number_of_countries_in_db),
                                            user_id=user.id)
            self.repo.add(new_airline)

    def generate_flights_per_company(self, num):
        airlines = self.repo.get_all(AirlineCompanies)
        for a in airlines:
            for i in range(num):
                airline_company_id = a.id
                origin_country_id = random.randint(1, self.number_of_countries_in_db)
                destination_country_id = random.randint(1, self.number_of_countries_in_db)
                departure_time = self.fake.date_time_between(start_date='now', end_date='+2y')
                landing_time = departure_time + timedelta(hours=random.randint(2, self.max_hours_delta_t))  # min delta t is 2 hours
                remaining_tickets = self.remaining_tickets_per_flight
                self.repo.add(Flights(  airline_company_id=airline_company_id,
                                        origin_country_id=origin_country_id,
                                        destination_country_id=destination_country_id,
                                        departure_time=departure_time,
                                        landing_time=landing_time,
                                        remaining_tickets=remaining_tickets))

    def generate_tickets_per_customer(self, num):
        customers = self.repo.get_all(Customers)
        flights = self.repo.get_all(Flights)
        for c in customers:
            shuffled_flights = random.sample(flights, len(flights))
            flights_for_tickets = shuffled_flights[0:num]
            for f in flights_for_tickets: self.repo.add(Tickets(flight_id=f.id,
                                                                customer_id=c.id))