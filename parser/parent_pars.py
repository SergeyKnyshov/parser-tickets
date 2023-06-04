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
    
    def format_date_to_datetime(self, date_str):
        return datetime.datetime.strptime(f"{date_str}", "%d.%m.%Y")
        
    def format_time_to_datetime(self, time_str):
        return datetime.datetime.strptime(time_str, "%H:%M")#.time()
        
