from  bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_ADDRESS = 'dbtest.c0odp5hguxv4.us-west-2.rds.amazonaws.com' ## INSERT YOUR DB ADDRESS IF IT'S NOT ON PANOPLY
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = "derek" ## CHANGE THIS TO YOUR PANOPLY/POSTGRES USERNAME
POSTGRES_PASSWORD = 'temp1234' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES PASSWORD
POSTGRES_DBNAME = 'financial' ## CHANGE THIS TO YOUR DATABASE NAME
# A long string that contains the necessary Postgres login information
postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME, password=POSTGRES_PASSWORD, ipaddress=POSTGRES_ADDRESS,port=POSTGRES_PORT, dbname=POSTGRES_DBNAME))


db =create_engine(postgres_str)

base = declarative_base()

class News2(base):
    __tablename__ = 'news'
    new_id = Column(Integer, primary_key=True)
    date = Column(String)
    heading = Column(String)
    url = Column(String)
    summary = Column(String)

Session = sessionmaker(db)

session = Session()

base.metadata.create_all(db)
session.commit()

# Read
news_in_db = session.query(News2)
for new in news_in_db:
    print(new.new_id)