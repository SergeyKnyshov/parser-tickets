from .parent_pars import Parser
from bs4 import BeautifulSoup
import datetime
import re
from tqdm import tqdm

class ParserRailway(Parser):

    def get_tickets(self):

        lst_of_ticket = self.html.find_all('div', 'wg-train-options__wrap')
        lst = []
        for q in tqdm(lst_of_ticket):
            query = self.get_route(q)
            lst.append(query)
            
        return lst
    
    def __get_origin_city(self, ticket):
            return ticket.find_all('span', 'wg-track-info__direction')[0].text

    def __get_destination_city(self, ticket):
        return ticket.find_all('span', 'wg-track-info__direction')[1].text

    def __get_plackart_price(self, ticket):
        a = ticket.find_all('span', 'wg-wagon-type__price-value')[0].text
        return ''.join([el for el in a if el in '0123456789'])

    def __get_cupe_price(self, ticket):
        ticket = ticket.find_all('span', 'wg-wagon-type__price-value')
        if len(ticket) == 1:
            res = ticket[0].text
        else:
            res = ticket[1].text
        
        return self.__edit_price(res)
    
    def __get_origin_date(self, ticket):
        origin_time = ticket.find_all('span', 'wg-track-info__time')[0].text
        origin_date = ticket.find_all('span', 'wg-track-info__date')[0].text
        origin_date = self.format_date(origin_date)
        
        return datetime.datetime.strptime(f'{origin_date} {origin_time}', '%d.%m.%Y %H:%M')

    def __get_destination_date(self, ticket):
        dest_time = ticket.find_all('span', 'wg-track-info__time')[1].text
        dest_date = ticket.find_all('span', 'wg-track-info__date')[1].text
        dest_date = self.format_date(dest_date)
        
        return datetime.datetime.strptime(f'{dest_date} {dest_time}', '%d.%m.%Y %H:%M')

    def __get_duration(self, ticket):
        date1 = self.__get_origin_date(ticket)
        date2 = self.__get_destination_date(ticket)
        return date2 - date1

    def __get_origin_station(self, ticket):
        t = ticket.find_all('span', 'wg-track-info__station')[0].text
        if t == '':
            t = None
        return t

    def __get_destination_station(self, ticket):
        t = ticket.find_all('span', 'wg-track-info__station')[0].text
        if t == '':
            t = None
        return t
    
    def get_route(self, html_of_ticket):

        flight_dict = {'origin_city':self.__get_origin_city(html_of_ticket),
                'destination_city':self.__get_destination_city(html_of_ticket),
                'price':self.__get_plackart_price(html_of_ticket),
                'company':'РЖД',
                'origin_date':self.__get_origin_date(html_of_ticket),
                'destination_date':self.__get_destination_date(html_of_ticket),
                'duration':'',#self.__get_duration(html_of_ticket),
                'types':'Train'
        }
        return flight_dict
    
    def __edit_price(self, price):

        return re.search(r'\d+[ ]?\d+[,]?\d+?', price)[0]