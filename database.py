from datetime import datetime
from environs import Env

import psycopg2

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


env = Env()
env.read_env(None)

engine = create_engine(f"postgresql+psycopg2://{env('DB_USERNAME')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}")
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class Statement(Base):
    __tablename__ = 'statement'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    career = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    company = Column(String, nullable=False)
    text = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    stir = Column(String, nullable=False)
    is_new = Column(Boolean, default=True)
    created = Column(Date, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship('Users', back_populates='statements')


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    statements = relationship('Statement', back_populates='user')
    

Base.metadata.create_all(engine)