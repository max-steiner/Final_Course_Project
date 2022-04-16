from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class Administrators(Base):
    __tablename__ = 'administrators'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False, unique=True)
    last_name = Column(Text(), nullable=False, unique=True)
    user_id = Column(BigInteger(),  ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    users = relationship('Users', backref=backref('administrators', uselist=True, passive_deletes=True))

    __table_args__ = (UniqueConstraint('first_name', 'last_name', name='una_1'),)

    def __repr__(self):
        return f'''\n<<Administrator id={self.id}>>
         First name={self.first_name} 
         Last name={self.last_name} 
         User id={self.user_id}'''

    def __str__(self):
        return f'''\n<<Administrator id={self.id}>>
         First name={self.first_name} 
         Last name={self.last_name} 
         User id={self.user_id}'''
