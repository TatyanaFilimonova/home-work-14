from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .SQLalchemy_classes import Base
import os

POSTGRES_DB = os.environ.get('BD_HOST', "localhost")
engine = create_engine(
    "postgresql+psycopg2://postgres:1234@"+POSTGRES_DB+"/scrapy", echo=True)
DBSession = sessionmaker(bind=engine)
Base.metadata.bind = engine
pgsession = DBSession()
