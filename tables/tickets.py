from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(),  ForeignKey('flights.id', ondelete='CASCADE'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    customers = relationship('Customers', backref=backref('tickets', uselist=True, passive_deletes=True))
    flights = relationship('Flights', backref=backref('tickets', uselist=True, passive_deletes=True))

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_3'),)

    def __repr__(self):
        return f'''\n<<Ticket id: {self.id}>>
         Flight id: {self.flight_id} 
         Customer id: {self.customer_id}'''

    def __str__(self):
        return f'''\n<<Ticket id: {self.id}>>
        Flight id: {self.flight_id} 
        Customer id: {self.customer_id}'''
