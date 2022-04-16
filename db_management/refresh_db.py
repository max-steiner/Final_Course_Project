from db_management.db_config import local_session, create_all_entities
from db_management.db_repo import DbRepo
from datetime import datetime
from tables.countries import Countries
from tables.flights import Flights
from tables.tickets import Tickets
from tables.airline_companies import AirlineCompanies
from tables.customers import Customers
from tables.users import Users
from tables.user_roles import UserRoles
from tables.administrators import Administrators
from logger import Logger


repo = DbRepo(local_session)


def refresh_db():          # The special function for filling the database of tests information and updating it
    repo.delete_all_tables()
    create_all_entities()
    logger = Logger.get_instance()
    repo.reset_db()                             # database cleanup
    repo.add_all([Countries(name='Israel'),     # database filling
                  Countries(name='USA'),
                  Countries(name='France'),
                  Countries(name='Russia')])
    repo.add_all([UserRoles(role_name='Administrator'),
                  UserRoles(role_name='Airline company'),
                  UserRoles(role_name='Customer'),
                  UserRoles(role_name='Anonymous')])
    repo.add_all(
                 [Users(username='ron_michael', password='Ron123', email='michael@mail.com', user_role=1),
                  Users(username='rami_shaul', password='Rami123', email='shaul@mail.com', user_role=1),
                  Users(username='meyer_steiner', password='Meyer123', email='steiner@mail.com', user_role=3),
                  Users(username='mahmud_abbas', password='Mahmud123', email='rabbas@mail.com', user_role=3),
                  Users(username='liora_friedman', password='Liora123', email='friedman@mail.com', user_role=3),
                  Users(username='sara_bergman', password='Sara123', email='bergman@mail.com', user_role=3),
                  Users(username='mark_dayan', password='Mark123', email='dayan@mail.com', user_role=3),
                  Users(username='malka_tsimerman', password='Malka123', email='tsimerman@mail.com', user_role=3),
                  Users(username='hana_mor', password='Hana123', email='mor@mail.com', user_role=4),
                  Users(username='lidor_hazan', password='Lidor123', email='hazan@mail.com', user_role=4),
                  Users(username='el_al', password='elal123', email='el_al@mail.com', user_role=2),
                  Users(username='american_airlines', password='America123', email='america@mail.com', user_role=2),
                  Users(username='air_france', password='France123', email='france@mail.com', user_role=2),
                  Users(username='aeroflot', password='Aeroflot123', email='aeroflot@mail.com', user_role=2),
                  Users(username='israir', password='Israir123', email='israir@mail.com', user_role=2)]
    )
    repo.add_all(
        [Administrators(first_name='Ron', last_name='Michael', user_id=1),
         Administrators(first_name='Rami', last_name='Shaul', user_id=2)]
    )
    repo.add_all(
        [AirlineCompanies(name='El Al', country_id=1, user_id=11),
         AirlineCompanies(name='American Airlines', country_id=2, user_id=12),
         AirlineCompanies(name='Air France', country_id=3, user_id=13),
         AirlineCompanies(name='Aeroflot', country_id=4, user_id=14),
         AirlineCompanies(name='Israir', country_id=1, user_id=15)]
    )
    repo.add_all(
                 [Customers(first_name='Meyer', last_name='Steiner',
                            address='Israel, Ashdod, st. Sitrin 1/25',
                            phone_number='054-972-00-28',
                            credit_card_number='1234 5679 2345 6789',
                            user_id=3),
                  Customers(first_name='Mahmud', last_name='Abbas',
                            address='Israel, Tel Aviv, st. Dezingof 2/15',
                            phone_number='053-875-35-22',
                            credit_card_number='9586 5349 545 3439',
                            user_id=4),
                  Customers(first_name='Liora', last_name='Friedman',
                            address='Israel, Natanya, st. Jabotincky 34/12',
                            phone_number='054-685-00-21',
                            credit_card_number='2345 5436 5342 9879',
                            user_id=5),
                  Customers(first_name='Mark', last_name='Dayan',
                            address='Israel, Haifa, st. Rotshild 14/22',
                            phone_number='052-485-18-18',
                            credit_card_number='4563 4123 8765 5436',
                            user_id=6)]
    )
    repo.add_all(
                 [Flights(airline_company_id=1,
                          origin_country_id=1,
                          destination_country_id=2,
                          departure_time=datetime(2022, 3, 1, 10, 30),
                          landing_time=datetime(2022, 3, 1, 14, 19, 30),
                          remaining_tickets=35),
                  Flights(airline_company_id=2,
                          origin_country_id=2,
                          destination_country_id=3,
                          departure_time=datetime(2022, 3, 2, 6, 0, 10),
                          landing_time=datetime(2022, 3, 2, 10, 0, 10),
                          remaining_tickets=14),
                  Flights(airline_company_id=3,
                          origin_country_id=3,
                          destination_country_id=4,
                          departure_time=datetime(2022, 3, 3, 8, 15, 10),
                          landing_time=datetime(2022, 3, 3, 14, 30, 10),
                          remaining_tickets=42),
                  Flights(airline_company_id=5,
                          origin_country_id=1,
                          destination_country_id=3,
                          departure_time=datetime(2022, 3, 10, 11, 20, 10),
                          landing_time=datetime(2022, 3, 10, 15, 20, 10),
                          remaining_tickets=0),
                  Flights(airline_company_id=4,
                          origin_country_id=4,
                          destination_country_id=1,
                          departure_time=datetime(2022, 3, 12, 19, 30, 10),
                          landing_time=datetime(2022, 3, 12, 14, 23, 10),
                          remaining_tickets=100)]
                )
    repo.add_all(
        [Tickets(flight_id=1, customer_id=1),
         Tickets(flight_id=1, customer_id=2),
         Tickets(flight_id=2, customer_id=4),
         Tickets(flight_id=3, customer_id=2),
         Tickets(flight_id=5, customer_id=3)]
                     )

    repo.create_all_stored_procedures(
        "C:/Users/User/PycharmProjects/Final_Course_Project/db_management/stored_procedures_db")
    logger.logger.critical('The data base  has been successfully refreshed')


refresh_db()

res = repo.get_by_id(Flights, id_=20)
print(res)



