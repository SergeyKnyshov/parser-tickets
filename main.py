import datetime
date1 = datetime.datetime.today()
date2 = datetime.timedelta(hours=1)
date1 += date2
date1 = date1 - datetime.datetime.today()
print(datetime.datetime(0, 0, 0))
