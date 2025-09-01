from sqlalchemy import Integer, String, Column, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Weather(Base):

    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    condition = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
