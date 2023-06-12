from .pars_aviasales import ParserAviaSales
from .pars_railway import ParserRailway
from crawler.crawl_aviasales import CrawlerAviaSales
from crawler.crawl_railway import CrawlerRailway
from Database.dbhelp import DBhelper
# from ..Database.dbase import *
from tqdm import tqdm

class ParserController:
    def __init__(self, origin, destination, date, engine):
        self.origin = origin
        self.destination = destination
        self.date = date
        
    def get_tickets(self):
        crawl_web1 = self.__get_avia_tickets()
        crawl_web2 = self.__get_rail_tickets()
        
        lst_of_tickets = []
        lst_of_tickets.extend(crawl_web1)
        lst_of_tickets.extend(crawl_web2)
        
        return lst_of_tickets
        
        
    def __get_avia_tickets(self):
        crawl = CrawlerAviaSales(self.origin, self.destination, self.date)
        crawl_web = crawl.get_html()
        
        pars = ParserAviaSales(crawl_web)
        return pars.get_tickets()
    
    def __get_rail_tickets(self):
        crawl = CrawlerRailway(self.origin, self.destination, self.date)
        crawl_web = crawl.get_html()
        
        pars = ParserRailway(crawl_web)
        return pars.get_tickets()
    
    def add_tickets_into_db(self, lst_of_tickets):
        db = DBhelper(engine)
        
        for el in tqdm(lst_of_tickets):
            db.add_ticket(el)
            
        
        
        
    