from sqlalchemy import Column, BigInteger,  Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False, unique=True)
    last_name = Column(Text(), nullable=False, unique=True)
    address = Column(Text(), nullable=False, unique=False)
    phone_number = Column(Text(), nullable=False, unique=True)
    credit_card_number = Column(Text(), nullable=False, unique=True)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    users = relationship('Users', backref=backref('customers', uselist=True, passive_deletes=True))
    
    __table_args__ = (UniqueConstraint('first_name', 'last_name', name='una_2'),)

    def __repr__(self):
        return f'''\n<<Customer id={self.id} >> 
        First name: {self.first_name} 
        Last name: {self.last_name} 
        Address: {self.address} 
        Phone number: {self.phone_number} 
        Credit-card number: {self.credit_card_number} 
        User id: {self.user_id}'''

    def __str__(self):
        return f'''\n<<Customer id={self.id}>> 
        First name: {self.first_name} 
        Last name: {self.last_name} 
        Address: {self.address} 
        Phone number: {self.phone_number} 
        Credit-card number: {self.credit_card_number} 
        User id: {self.user_id}'''
