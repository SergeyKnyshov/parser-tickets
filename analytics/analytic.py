from parser.pars_controller import ParserController
from .world_map import Map
from .coords import geoloc

class AnalyticsController:
    def __init__(self, lst_of_cities, turn):
        self.lst_of_cities = lst_of_cities  ## [(Чел, 13.06), [(Волг), Сочи, Калин], [] Моск]
        self.map = Map()
        if turn == 'price':
            self.turn = 'price'
        elif turn == 'time':
            self.turn = 'time'
            
        
        
    def build_route(self):
        
        lst = self.lst_of_cities
        
        dict_lst = []
        
        for i in range(len(lst)):
            if type(lst[i]) is tuple and type(lst[i+1]) is list:
                for el in lst[i+1]:
                    route = ParserController((lst[i][0], el[0], lst[i][1]))  ## город, дата, город
                    
                    route_tickets = route.get_tickets_from_web()
                    if not route_tickets:  ## Если есть в базе данных
                        route_tickets = route.get_tickets_from_db((lst[i][0], el[0]))
                        
                    route_ticket = self.__get_right_route(route_tickets)
                    coords = self.__unpack_dict_to_coords(route_ticket)
                    self.map.add_way(coords[0], coords[1])
                    
            elif type(lst[i]) is list and type(lst[i+1]) is list:
                for elem in lst[i]:
                    for el in lst[i+1]:
                        route = ParserController((elem[0], el[0], elem[1]))
                        
                        route_tickets = route.get_tickets_from_web()
                        if not route_tickets:
                            route_tickets = route.get_tickets_from_db((elem[0], el[0]))
                            
                        route_ticket = self.__get_right_route(route_tickets)    
                        coords = self.__unpack_dict_to_coords(route_ticket)
                        self.map.add_way(coords[0], coords[1])
            
            elif type(lst[i]) is list and lst[i+1] == lst[-1]:
                for el in lst[i]:
                    route = ParserController((el[0], lst[i+1], el[1]))
                        
                    route_tickets = route.get_tickets_from_web()
                    if not route_tickets:
                        route_tickets = route.get_tickets_from_db((el[0], lst[i+1][0]))
                        
                    route_ticket = self.__get_right_route(route_tickets)
                    coords = self.__unpack_dict_to_coords(route_ticket)
                    self.map.add_way(coords[0], coords[1])
            else:
                print('ERROR!')
                        
                

    def __unpack_dict_to_coords(self, dict_of_way):

        coords = (dict_of_way['origin_city'], dict_of_way['destination_city'])

        
        orig_coords = geoloc.geocode(coords[0])
        dest_coords = geoloc.geocode(coords[1])
        
        return [(orig_coords.longitude, dest_coords.longitude), (orig_coords.latitude, dest_coords.latitude)]
        

    def __get_right_route(self, lst_of_tickets):
        if self.turn == 'price':
            res = self.__get_min_price(lst_of_tickets)
        elif self.turn == 'time':
            res = self.__get_min_time(lst_of_tickets)
            
        return res
        
    def __get_min_time(self, lst):
        lst_of_min_time = []

        for el in lst:
            lst_of_min_time.append(el['duration'])
        min_time = max(lst)
        for el in lst:
            if el['duration'] == min_time:
                res = el
        return res
    
    def __get_min_price(self, lst):
        lst_of_min_price = []

        for el in lst:
            lst_of_min_price.append(int(el['price']))
        min_price = min(lst_of_min_price)
        for el in lst:
            if int(el['price']) == min_price:
                res = el
                
        return res
        
        