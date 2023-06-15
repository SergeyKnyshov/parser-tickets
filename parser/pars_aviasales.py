from .parent_pars import Parser
from bs4 import BeautifulSoup
import datetime
from tqdm import tqdm

class ParserAviaSales(Parser):

    def get_tickets(self):
        
        lst_of_ticket = self.html.find_all('div', 'ticket-desktop')
        lst = []
        for q in lst_of_ticket:
            query = self.get_route(q)
            if query["company"] != None:
                lst.append(query)
        return lst
            
    def __get_origin_city(self, ticket):
        cities = ticket.find_all('div', class_ = 'segment-route__city')
        origin_city = cities[0].text
        return origin_city

    def __get_destination_city(self, ticket):
        cities = ticket.find_all('div', class_ = 'segment-route__city')
        destination_city = cities[1].text
        return destination_city

            
    def __get_price(self, ticket):
        price = ticket.find('div', class_ = "ticket-desktop__side-container").find('span').text.replace('\u202f', '').replace('\u2009₽', '')
        return price

        
    def __get_airline(self, ticket):
        try:
            airline = ticket.find('div', class_ = "ticket-desktop__content").find_all('div', attrs = {'data-test-id': 'text'})[0].text
        except:
            airline = None        
        return airline   
            
    def __get_origin_date(self, ticket):
        origin_time = ticket.find('div', class_ = 'segment-route__endpoint origin').find('div', attrs = {'data-test-id': 'time'}).text
        origin_date = ticket.find_all('div', class_ = 'segment-route__date')[0].text
        
        date = self.format_date(origin_date)  ## 03.02.2023     
        res = datetime.datetime.strptime(f'{date} {origin_time}', '%d.%m.%Y %H:%M')
        return res

    def __get_destination_date(self, ticket):
        destination_time = ticket.find('div', class_ = 'segment-route__endpoint destination').find('div', attrs = {'data-test-id': 'time'}).text
        destination_date = ticket.find_all('div', class_ = 'segment-route__date')[1].text
        
        date = self.format_date(destination_date)
        res = datetime.datetime.strptime(f'{date} {destination_time}', '%d.%m.%Y %H:%M')
        return res        
    
    def __get_origin_airport(self, ticket):
        origin_airport = ticket.find('div', class_ = 'segment-route__path-endpoint --departure --plane').find('span').text
        return origin_airport
            
    def __get_destination_airport(self, ticket):
        destination_airport = ticket.find('div', class_ = 'segment-route__path-endpoint --arrival --plane').find('span').text
        return destination_airport
    
    def __get_duration(self, ticket):
        date1 = self.__get_origin_date(ticket)
        date2 = self.__get_destination_date(ticket)
        return date2 - date1
    
    def get_route(self, html_of_ticket):

        flight_dict = {'origin_city':self.__get_origin_city(html_of_ticket),
                'destination_city':self.__get_destination_city(html_of_ticket),
                'price':self.__get_price(html_of_ticket),
                'company':self.__get_airline(html_of_ticket),
                'origin_date':self.__get_origin_date(html_of_ticket),
                'destination_date':self.__get_destination_date(html_of_ticket),
                # 'duration':'',#self.__get_duration(html_of_ticket),
                'types':'Plane'
        }
        return flight_dict