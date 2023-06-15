from parser.pars_controller import ParserController
from .world_map import Map
from .coords import geoloc

class AnalyticsController:
    def __init__(self, lst_of_cities, turn):
        self.lst_of_cities = lst_of_cities  ## [(Чел, 13.06), [(Волг), Сочи, Калин], [] Моск]
        self.turn = turn
        self.map = Map()
        
        
    def build_full_route(self):
        
        lst = self.lst_of_cities
        
        # dict_lst = []
        
        for i in range(len(lst)-1):
            if type(lst[i]) is tuple and type(lst[i+1]) is list:  ## первый город-список
                for el in lst[i+1]:
                    dep_city = lst[i][0]
                    des_city = el[0]
                    dep_date = lst[i][1]
                    
                    self.build_route_edge(dep_city, des_city, dep_date)    
                    
            elif type(lst[i]) is list and type(lst[i+1]) is list:  ## список-список
                for fst_lst_el in lst[i]:
                    for sec_lst_el in lst[i+1]:
                        dep_city = fst_lst_el[0]
                        des_city = sec_lst_el[0]
                        dep_date = fst_lst_el[1]
                        
                        self.build_route_edge(dep_city, des_city, dep_date)
                
            
            elif type(lst[i]) is list and lst[i+1] == lst[-1]:  ##  список-последний город
                for el in lst[i]:
                    dep_city = el[0]
                    des_city = lst[i+1][0]
                    dep_date = el[1]
                    
                    self.build_route_edge(dep_city, des_city, dep_date)
                    
            elif type(lst[i]) is list and type(lst[i+1]) is tuple and lst[i+1] != lst[-1]:  ##  список-город
                for el in lst[i]:
                    dep_city = el[0]
                    des_city = lst[i+1][0]
                    dep_date = el[1]
                    
                    self.build_route_edge(dep_city, des_city, dep_date)
                    
            elif type(lst[i]) is tuple and type(lst[i+1]) is tuple and lst[i+1] != lst[-1]:  ## первый город-город
                    dep_city = lst[i][0]
                    des_city = lst[i+1][0]
                    dep_date = lst[i][1]
                    
                    self.build_route_edge(dep_city, des_city, dep_date)
                    
            elif type(lst[i]) is tuple and lst[i+1] == lst[-1]:  ##  город-последний город
                    dep_city = lst[i][0]
                    des_city = lst[i+1]
                    dep_date = lst[i][1]
                    
                    self.build_route_edge(dep_city, des_city, dep_date)
                    
            else:
                print('ERROR!')
                    
    def build_route_edge(self, depart_city, destin_city, date):      
        
        route = ParserController(depart_city, destin_city, date)  ## город, дата, город
        
        lst_of_route_tickets = route.get_tickets_from_web()
        if lst_of_route_tickets == False:  ## Если есть в базе данных
            rout_tickets = route.get_tickets_from_db(depart_city, destin_city)
        else:
            rout_tickets = lst_of_route_tickets
        
        rout_tickets = self.__add_duration_into_dict(rout_tickets)
        route_ticket = self.__get_right_route(rout_tickets)
        coords = self.__unpack_dict_to_coords(route_ticket)
        self.map.add_way(coords[0], coords[1], route_ticket)

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
        min_time = min(lst_of_min_time)
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
    
    def __add_duration_into_dict(self, lst_of_dict):
        for el in lst_of_dict:
            el['duration'] = el['destination_date'] - el['origin_date']
            
        return lst_of_dict
        
        