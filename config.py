import os
from peewee import PostgresqlDatabase
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    os.getenv('POSTGRES_DB'),
    user='svyat',
    password=os.getenv('POSTGRES_PASSWORD'),
    host='localhost'
)

token = os.getenv('TOKEN')

el_search = Elasticsearch(os.getenv('ELASTICSEARCH_URL'))
