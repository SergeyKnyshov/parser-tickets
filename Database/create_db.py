from .models import Base 

## 'sqlite:///Trips.db'

def init_schema(engine):
    Base.metadata.create_all(bind=engine)