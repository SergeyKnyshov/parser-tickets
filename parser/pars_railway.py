from parent_pars import Parser
from bs4 import BeautifulSoup
import datetime
import re

class ParserRailway(Parser):

    def get_tickets(self):

        lst_of_ticket = self.html.find_all('div', 'wg-train-options__wrap')
        lst = []
        for q in lst_of_ticket:
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
    
    def __get_origin_time(self, ticket):
        return self.format_time_to_datetime(ticket.find_all('span', 'wg-track-info__time')[0].text)

    def __get_destination_time(self, ticket):
        return self.format_time_to_datetime(ticket.find_all('span', 'wg-track-info__time')[1].text)

    def __get_origin_dates(self, ticket):
        t = ticket.find_all('span', 'wg-track-info__date')[0].text
        res = self.format_date(t)
        return self.format_date_to_datetime(res)

    def __get_destination_dates(self, ticket):
        t = ticket.find_all('span', 'wg-track-info__date')[1].text
        res = self.format_date(t)
        return self.format_date_to_datetime(res)

    def __get_duration(self, ticket):
        return self.format_duration(ticket.find('span', 'wg-track-info__duration-time').text)

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
                'airline':None,
#                 'origin_time':self.__get_origin_time(html_of_ticket),
#                 'destination_time':self.__get_destination_time(html_of_ticket),
#                 'origin_dates':self.__get_origin_dates(html_of_ticket),
#                 'destination_dates':self.__get_destination_dates(html_of_ticket),
                'duration':self.__get_duration(html_of_ticket),
                'types':'Train'
        }
        return flight_dict
    
    def __edit_price(self, price):

        return re.search(r'\d+[ ]?\d+[,]?\d+?', price)[0]