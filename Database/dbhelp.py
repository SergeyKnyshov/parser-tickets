from Database.create_db import init_schema
from Database.models import City, Trip, Company
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import select, table, column

from geopy.geocoders import Bing
from analytics.coords import geoloc
## 'sqlite:///Trips.db'
class DBhelper:
    def __init__(self, path):
        self.engine = create_engine(path)
        self.session = sessionmaker(self.engine)
        init_schema(self.engine)
    
    def check_exist_trip_by_route(self, origin_city, destination_city):
        
        try:
            orig_city_id = self.__get_city_id(origin_city)
            dest_city_id = self.__get_city_id(destination_city)
        except:
            orig_city_id = None
            dest_city_id = None
            
        if orig_city_id and dest_city_id:
            with self.session.begin() as session:
                ex_trip = select(Trip).where(
                    Trip.origin_city_id == orig_city_id,
                    Trip.destination_city_id == dest_city_id
                )
            
                trip = session.scalar(ex_trip)
                if trip:
                    return True
                else:
                    return False
        else:
            return False
    
    def check_exist_trip(self, trip_dict):
        with self.session.begin() as session:
            ex_trip = select(Trip).where(
                Trip.price == trip_dict['price'],
                Trip.origin_date == trip_dict['origin_date'],
                Trip.destination_date == trip_dict['destination_date'],
            )
        
            trip = session.scalar(ex_trip)
            if trip:
                return True
            else:
                return False
            
    def __check_exist_city(self, city_to_add):
        with self.session.begin() as session:
            ex_route = select(City).where(
                City.city == city_to_add
            )
            
            try:
                route = session.scalar(ex_route)
                return route
            except:
                return False
            
    def __check_exist_company(self, company_to_add):
        with self.session.begin() as session:
            ex_airline = select(Company).where(
                Company.company == company_to_add
            )
            
            airline = session.scalar(ex_airline)
            if airline:
                return True
            else:
                return False
    
    def __add_city(self, city_to_add):
        with self.session.begin() as session:
            if not self.__check_exist_city(city_to_add):
                city = City(
                    city = city_to_add
                )

                session.add(city)
                session.commit()
            else:
                return
            
            
    def __add_company(self, company_to_add):
        with self.session.begin() as session:  
            if not self.__check_exist_company(company_to_add):
                airl = Company(
                    company = company_to_add
                )

                session.add(airl)
                session.commit()
            else:
                return
            
    def __get_city_id(self, city):
        with self.session.begin() as session:  
            city = select(City).where(
                City.city == city
            )
            
            return session.scalar(city).city_id
        
    def __get_company_id(self, company):
        with self.session.begin() as session:  
            airline = select(Company).where(
                Company.company == company
            )
            
            return session.scalar(airline).company_id
        
    def __add_trip(self, trip_dict):

        with self.session.begin() as session:
            if not self.check_exist_trip(trip_dict):
                trip = Trip(
                    origin_city_id = self.__get_city_id(trip_dict['origin_city']),
                    destination_city_id = self.__get_city_id(trip_dict['destination_city']),
                    company_id = self.__get_company_id(trip_dict['company']),
                    price = trip_dict['price'], 
                    origin_date = trip_dict['origin_date'],  
                    destination_date = trip_dict['destination_date'],  
                    # duration = trip_dict['duration'],  
                    types = trip_dict['types']
                )

                session.add(trip)
                session.commit()
                print("Рейс успешно добавлен в базу данных.")
            else:
                return

    def __get_city_by_id(self, city_id):
        with self.session.begin() as session:
            city = select(City).where(
                City.city_id == city_id
            )
            
            return session.scalar(city).city
        
    def __get_company_by_id(self, comp_id):
        with self.session.begin() as session:
            company = select(Company).where(
                Company.company_id == comp_id
            )
            
            return session.scalar(company).company
    
    def add_ticket(self, trip_dict):
        self.__add_city(trip_dict['origin_city'])
        self.__add_city(trip_dict['destination_city'])
        self.__add_company(trip_dict['company'])
        self.__add_trip(trip_dict)
        
    def get_trip(self, origin_city, destination_city):
        orig_city_id = self.__get_city_id(origin_city)
        dest_city_id = self.__get_city_id(destination_city)
        with self.session.begin() as session:
            try:
                trip = select(Trip).where(
                    Trip.origin_city_id == orig_city_id,
                    Trip.destination_city_id == dest_city_id
                )
            except:
                print(f'Маршрут {origin_city}-{destination_city} отсутствует в базе, идет подкачка...')
            
            res = session.scalars(trip)
            result = []
            
            for el in res:
                # duration = el.destination_date - el.origin_date
            
                trip_dict = {'origin_city': origin_city,
                        'destination_city': destination_city,
                        'price': el.price,
                        'company':self.__get_company_by_id(el.company_id),
                        'origin_date':el.origin_date,
                        'destination_date':el.destination_date,
                        # 'duration': duration,
                        'types':el.types
                }
                
                result.append(trip_dict)
        return result
        