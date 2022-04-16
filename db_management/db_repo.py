from sqlalchemy import asc
from tables.countries import Countries
from tables.flights import Flights
from tables.tickets import Tickets
from tables.airline_companies import AirlineCompanies
from tables.customers import Customers
from tables.users import Users
from tables.user_roles import UserRoles
from tables.administrators import Administrators


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')

    def reset_db(self):
        self.reset_auto_inc(Countries)
        self.reset_auto_inc(Users)
        self.reset_auto_inc(AirlineCompanies)
        self.reset_auto_inc(Customers)
        self.reset_auto_inc(Flights)
        self.reset_auto_inc(Tickets)
        self.reset_auto_inc(Administrators)
        self.reset_auto_inc(UserRoles)

    def delete_table(self, table_name):
        self.local_session.execute(f'drop TABLE if exists {table_name} cascade')
        self.local_session.commit()

    def delete_all_tables(self):
        self.delete_table('countries')
        self.delete_table('flights')
        self.delete_table('tickets')
        self.delete_table('airline_companies')
        self.delete_table('administrators')
        self.delete_table('customers')
        self.delete_table('users')
        self.delete_table('user_roles')

    def get_by_id(self, table_class, id_):
        return self.local_session.query(table_class).get(id_)

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def get_by_condition(self, table_class, cond):
        query_result = self.local_session.query(table_class)
        result = cond(query_result)
        return result

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_by_id(self, table_class, id_column_name, id_):
        self.local_session.query(table_class).filter(id_column_name == id_).delete(synchronize_session=False)
        self.local_session.commit()

    def update_by_id(self, table_class, id_column_name, id_, data):
        self.local_session.query(table_class).filter(id_column_name == id_).update(data)
        self.local_session.commit()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    def get_by_column_value(self, table_class, column_name, value):
        return self.local_session.query(table_class).filter(column_name == value).all()

    def get_by_ilike(self, table_class, column_name, exp):
        return self.local_session.query(table_class).filter(column_name.ilike(exp)).all()

    def create_all_stored_procedures(self, file):
        try:
            with open(file, 'r') as sp_file:
                queries = sp_file.read().split('|||')
            for query in queries:
                self.local_session.execute(query)
            self.local_session.commit()
            print('All store procedures were created')
        except FileNotFoundError():
            print('File was not found')
