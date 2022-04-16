from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_management.db_config import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False)
    email = Column(Text(), nullable=False, unique=True)
    user_role = Column(Integer(),  ForeignKey('user_roles.id', ondelete='CASCADE'), nullable=False)

    role = relationship('UserRoles', backref=backref('users', uselist=True, passive_deletes=True))

    def __repr__(self):
        return f'''\n<<User id: {self.id}>>
        Username: {self.username} 
        Password: {self.password} 
        Email: {self.email} 
        User role: {self.user_role}\n'''

    def __str__(self):
        return f'''\n<<User id: {self.id}>>
        Username: {self.username} 
        Password: {self.password} 
        Email: {self.email} 
        User role: {self.user_role}\n'''
