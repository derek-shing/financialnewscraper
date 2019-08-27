from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from  bs4 import BeautifulSoup
import requests


POSTGRES_ADDRESS = 'dbtest.c0odp5hguxv4.us-west-2.rds.amazonaws.com' ## INSERT YOUR DB ADDRESS IF IT'S NOT ON PANOPLY
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = "" ## CHANGE THIS TO YOUR PANOPLY/POSTGRES USERNAME
POSTGRES_PASSWORD = '' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES PASSWORD
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
#for new in news_in_db:
#    print(new.new_id)

def scrap_seeking_alpha():
    url = "https://seekingalpha.com/market-news"
    page = requests.get(url)
    soup = BeautifulSoup(page.text)
    news = soup.find(name="ul", attrs={'class':"item-list",'id':'latest-news-list'})



    root = "https://seekingalpha.com"
    id_list = [i['id'] for i in news.find_all(name='li', attrs={'class':'item'})]
    heading_list = [i.text for i in news.find_all('a')]
    url_list = [root+i['href'] for i in news.find_all('a')]
    date_list = [i['data-last-date'] for i in news.find_all(name='li', attrs={'class':'item'})]
    date_list2 = [i.split()[0] for i in date_list]
    id_list2 = [i.split('-')[2] for i in id_list]


    def db_contain_news(new_id):
        return session.query(News2).filter(News2.new_id==new_id).count()




    def getcontext(url):
        soup = BeautifulSoup(requests.get(url).text)
        contexts = soup.find_all(name='p', attrs={"class":"bullets_li"})
        i=0
        while (len(contexts)==0 and i<20 ):
            soup = BeautifulSoup(requests.get(url).text)
            contexts = soup.find_all(name='p', attrs={"class":"bullets_li"})
            i+=1
        context = [i.text for i in contexts]
        return context

    stop_index = len(id_list2)
    for i in range(len(id_list2)):
        if db_contain_news(id_list2[i]):
            stop_index = i
            break

    id_list2 = id_list2[:stop_index]
    date_list2 = date_list2[:stop_index]
    heading_list = heading_list[:stop_index]
    url_list = url_list[:stop_index]
    point_list = [getcontext(i) for i in url_list]

    for i in range(len(id_list2)):
        new = News2(new_id=id_list2[i], date=date_list2[i], heading=heading_list[i], summary=point_list[i],
                    url=url_list[i])
        session.add(new)
        session.commit()


    return



def handler(event, context):
    scrap_seeking_alpha()


    return {
        'stateCode':200,
        'message':' Hello from lambda function',
    }

#print(news_in_db[60].heading)