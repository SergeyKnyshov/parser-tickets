import datetime

d = {"origin_date":  datetime.datetime.now().replace(hour=3, minute=53, second=0, microsecond=0),
    "destination_date":  datetime.datetime.now().replace(hour=7, minute=24, second=0, microsecond=0)
}

d['duration'] = d['destination_date'] - d['origin_date']

print(d)