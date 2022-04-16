from sqlalchemy import Column, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class AirlineCompanies(Base):
    __tablename__ = 'airline_companies'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)
    country_id = Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    countries = relationship('Countries', backref=backref('airline_companies', uselist=True, passive_deletes=True))
    users = relationship('Users', backref=backref('airline_companies', uselist=True, passive_deletes=True))

    def __repr__(self):
        return f'''\n<<Airline name: {self.name}>>
        id: {self.id} 
        Country id: {self.country_id}
        User id: {self.user_id}'''

    def __str__(self):
        return f'''\n<<Airline name: {self.name}>>
        id: {self.id} 
        Country id: {self.country_id}
        User id: {self.user_id}'''
