from sqlalchemy import Column, BigInteger, Integer, DateTime, \
    ForeignKey
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id', ondelete='CASCADE'), nullable=False)
    origin_country_id = Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    destination_country_id = Column(BigInteger(),  ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    departure_time = Column(DateTime(), nullable=False)
    landing_time = Column(DateTime(), nullable=False)
    remaining_tickets = Column(Integer())

    airline_company = relationship(
        "AirlineCompanies", backref=backref("flights", uselist=True, passive_deletes=True))
    origin_country = relationship(
        "Countries", foreign_keys=[origin_country_id], uselist=True, passive_deletes=True)
    destination_country = relationship(
        "Countries", foreign_keys=[destination_country_id], uselist=True, passive_deletes=True)

    def __repr__(self):
        return f'''\n<<Flight id: {self.id}>>
        Airline Co. id: {self.airline_company_id} 
        Origin country id: {self.origin_country_id} 
        Destination country id: {self.destination_country_id} 
        Departure time: {self.departure_time} 
        Landing time: {self.landing_time} 
        Remaining tickets: {self.remaining_tickets}'''

    def __str__(self):
        return f'''\n<<Flight id={self.id} >>
        Airline Co. id: {self.airline_company_id} 
        Origin country id: {self.origin_country_id} 
        Destination country id: {self.destination_country_id} 
        Departure time: {self.departure_time} 
        Landing time: {self.landing_time} 
        Remaining tickets: {self.remaining_tickets}'''
