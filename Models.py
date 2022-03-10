from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, FLOAT

Base = declarative_base()


class Journey(Base):
    __tablename__ = "journeys_dravaib"
    id = Column(Integer, primary_key=True)
    source = Column(TEXT)
    destination = Column(TEXT)
    departure_datetime = Column(TIMESTAMP)
    arrival_datetime = Column(TIMESTAMP)
    carrier = Column(TEXT)
    vehicle_type = Column(TEXT)
    price = Column(FLOAT)
    currency = Column(String(3))
