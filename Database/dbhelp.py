from .create_db import init_schema
from .models import City, Trip, Company
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import select, table, column
## 'sqlite:///Trips.db'
class DBhelper:
    def __init__(self, path):
        self.engine = create_engine(path)
        self.session = sessionmaker(self.engine)
        
        init_schema(self.engine)
        
    def check_exist_trip(self, trip_dict):
        with self.session.begin() as session:
            ex_trip = select(Trip).where(
                Trip.price == trip_dict['price'],
                Trip.origin_date == trip_dict['origin_date'],
                Trip.destination_date == trip_dict['destination_date'],
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
                    company = trip_dict['company']
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
        
    def __get_company_id(self, trip_dict):
        with self.session.begin() as session:  
            airline = select(Company).where(
                Company.company == trip_dict['company']
            )
            
            return session.scalar(airline).id
        
    def __add_trip(self, trip_dict):

        with self.session.begin() as session:
            if not self.check_exist_trip(trip_dict):
                trip = Trip(
                    route_id = self.__get_city_id(trip_dict),
                    company_id = self.__get_company_id(trip_dict),
                    price = trip_dict['price'], 
                    origin_date = trip_dict['origin_date'],  
                    destination_date = trip_dict['destination_date'],  
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
        
    def find_ticket(self, req_dict):  ## словарь вида: откуда; куда; дата; компания; цена (yes/no); duration (yes/no)
        # if req_dict['company']: ## запрос по id требуемой компании           
        #     req_company_id = self.__get_company_id(req_dict['company'])
        # else:
        #     req_company_id = None
        
        if req_dict['price'] == 'yes':
            return self.__req_ticket_if_price(req_dict)
        elif req_dict['time'] == 'yes':
            pass
        elif req_dict['price'] == 'yes' and req_dict['time'] == 'yes':
            pass
        else:
            print("Error! Не был выбран не один из фильтров.")
            return
            
    def __req_ticket_if_price(self, req_dict):
        with self.session as session:
            min_price = select([func.min(Trip.price)])
            rout_id = self.__get_city_id(req_dict)
            trip = select(Trip).where(
                Trip.route_id == rout_id,
                Trip.origin_date == req_dict['origin_date'],
                Trip.price == min_price
            )
            return trip
    
    def __req_ticket_if_time(self, req_dict):
        with self.session as session:
            min_time = select([func.min(Trip.duration)])
            rout_id = self.__get_city_id(req_dict)
            trip = select(Trip).where(
                Trip.route_id == rout_id,
                Trip.origin_date == req_dict['origin_date'],
                Trip.duration == min_time
            )
            return trip
        
    def __req_ticket_if_price_and_time(self, req_dict):
        with self.session as session:
            min_price = select([func.min(Trip.price)])
            min_time = select([func.min(Trip.duration)])
            rout_id = self.__get_city_id(req_dict)
            trip = select(Trip).where(
                Trip.route_id == rout_id,
                Trip.origin_date == req_dict['origin_date'],
                Trip.price == min_price,
                Trip.duration == min_time
            )
            return trip