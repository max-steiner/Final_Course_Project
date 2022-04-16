from sqlalchemy import Column, Text, BigInteger
from db_management.db_config import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)

    def __repr__(self):
        return f'''\n<<Name: {self.name}>>
        Country id: {self.id}\n'''

    def __str__(self):
        return f'''\n<<Name: {self.name}>>
                Country id: {self.id}\n'''
