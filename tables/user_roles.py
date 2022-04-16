from sqlalchemy import Column, Integer, Text
from db_management.db_config import Base


class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    role_name = Column(Text(), unique=True, nullable=False)

    def __repr__(self):
        return f'''\n<<Role id: {self.id}>> 
        Role name: {self.role_name}'''

    def __str__(self):
        return f'''\n<<Role id: {self.id}>>
         Role name: {self.role_name}'''
