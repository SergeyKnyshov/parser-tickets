import sqlalchemy 
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import select
from dbase import *
class DBhelper:
    def __init__(self, engine):
        self.engine = create_engine(engine)
        self.session = sessionmaker(self.engine)
        
    def __check_exist_trip(self, trip_dict):
        with self.session.begin() as session:
            ex_trip = select(Trip).where(
                Trip.price == trip_dict['price'],
                Trip.origin_dates == trip_dict['origin_dates'],
                Trip.destination_dates == trip_dict['destination_dates'],
                Trip.duration == trip_dict['duration']
            )
        
            trip = session.scalar(ex_trip)
            if trip:
                return True
            else:
                return False
            
    def __check_exist_route(self, trip_dict):
        with self.session.begin() as session:
            ex_route = select(City).where(
                City.origin_city == trip_dict['origin_city'],
                City.destination_city == trip_dict['destination_city']
            )
            
            route = session.scalar(ex_route)
            if route:
                return True
            else:
                return False
            
    def __check_exist_company(self, trip_dict):
        with self.session.begin() as session:
            ex_airline = select(Company).where(
                Company.company == trip_dict['company'],
            )
            
            airline = session.scalar(ex_airline)
            if airline:
                return True
            else:
                return False
    
    def __add_city(self, trip_dict):
        with self.session.begin() as session:
            if not self.__check_exist_route(trip_dict):
                city = City(
                    origin_city = trip_dict['origin_city'],
                    destination_city = trip_dict['destination_city'] 
                )

                session.add(city)
                session.commit()
            else:
                return
            
    def __add_company(self, trip_dict):
        with self.session.begin() as session:  
            if not self.__check_exist_company(trip_dict):
                airl = Company(
                    airline = trip_dict['company']
                )

                session.add(airl)
                session.commit()
            else:
                return
            
    def __get_city_id(self, trip_dict):
        with self.session.begin() as session:  
            city = select(City).where(
                City.origin_city == trip_dict['origin_city'],
                City.destination_city == trip_dict['destination_city']
            )
            
            return session.scalar(city).id
        
    def __get_airline_id(self, trip_dict):
        with self.session.begin() as session:  
            airline = select(Company).where(
                Company.company == trip_dict['company']
            )
            
            return session.scalar(airline).id
        
    def __add_trip(self, trip_dict):

        with self.session.begin() as session:
            if not self.__check_exist_trip(trip_dict):
                trip = Trip(
                    route_id = self.__get_city_id(trip_dict),
                    company_id = self.__get_company_id(trip_dict),
                    price = trip_dict['price'], 
                    origin_dates = trip_dict['origin_dates'],  
                    destination_dates = trip_dict['destination_dates'],  
                    duration = trip_dict['duration'],  
                    types = trip_dict['types']
                )

                session.add(trip)
                session.commit()
                print("Рейс успешно добавлен в базу данных.")
            else:
                print('Такая запись уже существует!')
                return
            
    def add_ticket(self, trip_dict):
        self.__add_city(trip_dict)
        self.__add_company(trip_dict)
        self.__add_trip(trip_dict)
        
    def delete_ticket(self, trip_dict):
        pass