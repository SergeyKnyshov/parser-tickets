from .pars_aviasales import ParserAviaSales
from .pars_railway import ParserRailway
from crawler.crawl_aviasales import CrawlerAviaSales
from Database.dbhelp import DBhelper
from crawler.crawl_railway import CrawlerRailway
from tqdm import tqdm

class ParserController:
    def __init__(self, origin_city, destination_city, date):
        self.origin = origin_city
        self.destination = destination_city
        self.date = date
        self.engine = 'sqlite:///Trips.db'
        self.db = DBhelper(self.engine)
        
    def get_tickets_from_web(self):
        
        if not self.db.check_exist_trip_by_route(self.origin, self.destination):
            tickets_lst = []
            try:
                crawl_web1 = self.__get_avia_tickets_from_web()
                tickets_lst.extend(crawl_web1)
            except:
                print(f'Отсутствует маршрут {self.origin}-{self.destination} на aviasales')
            try:
                crawl_web2 = self.__get_rail_tickets_from_web()
                tickets_lst.extend(crawl_web2)
            except:
                print(f'Отсутствует маршрут {self.origin}-{self.destination} на РЖД')



            self.add_tickets_into_db(tickets_lst)
            
            return tickets_lst
        else:
            print(f'Маршрут {self.origin}-{self.destination} уже присутствует в базе данных!')
            return False
        
        
    def __get_avia_tickets_from_web(self):
        crawl = CrawlerAviaSales(self.origin, self.destination, self.date)
        crawl_web = crawl.get_html()
        
        pars = ParserAviaSales(crawl_web)
        return pars.get_tickets()
    
    def __get_rail_tickets_from_web(self):
        crawl = CrawlerRailway(self.origin, self.destination, self.date)
        crawl_web = crawl.get_html()
        
        pars = ParserRailway(crawl_web)
        return pars.get_tickets()
    
    def add_tickets_into_db(self, lst_of_tickets):
        
        for el in lst_of_tickets:
            self.db.add_ticket(el)
        
    def get_tickets_from_db(self, origin_city, destination_city):
        
        tick = self.db.get_trip(origin_city, destination_city)
        
        return tick
        
        
        
    