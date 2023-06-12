import sqlalchemy 
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///Trips.db')
class Base(DeclarativeBase): pass

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    origin_city = Column(String)
    destination_city = Column(String)

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company = Column(String)
    
class Trip(Base):
    __tablename__ = 'PlaneTrain'
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('cities.id'))
    airline_id = Column(Integer, ForeignKey('companies.id'))
    price = Column(String)
    origin_date = Column(DateTime)
    destination_date = Column(DateTime)
    duration = Column(DateTime)
    types = Column(String)
    TTL = Column(DateTime, server_default = func.now())

    origin_city = relationship("City", foreign_keys=[route_id])
    airline = relationship("companies")

Base.metadata.create_all(bind=engine)