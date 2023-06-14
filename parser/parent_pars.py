import datetime

class Parser:
    def __init__(self, html):
        self.html = html
    
    def get_tickets(self, html):
        pass
    

    def format_date(self, date):
        month = {"янв": "01", "фев": "02", "мар": "03", "апр": "04", 
            "мая": "05", "июн": "06", "июл": "07", "авг": "08", "сен": "09", 
            "окт": "10", "ноя": "11", "дек": "12"
        } 
        text = date.split()

        day = text[0]
        if len(day) == 1:
            day = '0' + str(day)
        mon = text[1][:3]
        mon = month[mon]
        res = day + '.' + mon + '.' +  str(datetime.datetime.now().year)

        return res

    def __get_origin_date(self, ticket):
        pass

    def __get_destination_date(self, ticket):
        pass        

    def get_duration(self):
        date1 = self.__get_origin_date()
        date2 = self.__get_destination_date()
        return date2 - date1
