import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    os.getenv('POSTGRES_DB'),
    user='postgres',
    password=os.getenv('POSTGRES_PASSWORD'),
    host='localhost'
)

TOKEN = os.getenv('TOKEN')
