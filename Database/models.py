from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass

class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city = Column(String)
    # orig_city_id = relationship("Trip", back_populates='city1')

class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    company = Column(String)
    comp_id = relationship('Trip', back_populates='comp')
    
    
class Trip(Base):
    __tablename__ = 'PlaneTrain'
    id = Column(Integer, primary_key=True)
    origin_city_id = Column(Integer, ForeignKey('cities.city_id'))
    destination_city_id = Column(Integer, ForeignKey('cities.city_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    price = Column(String)
    origin_date = Column(DateTime)
    destination_date = Column(DateTime)
    # duration = Column(DateTime, default=None, nullable=True)
    types = Column(String)
    TTL = Column(DateTime, server_default = func.now())

    # city1 = relationship("City", back_populates='orig_city_id')
    comp = relationship("Company", back_populates='comp_id')
    
    def get_ticket(self):
        return {
            
        }

