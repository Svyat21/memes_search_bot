from config import db
from peewee import Model, CharField, DateField, TextField
from search import add_to_index, remove_from_index, query_index
from aiogram.types import Message
import datetime


def db_connect(func):
    def wrapper(*args, **kwargs):
        db.connection()
        res = func(*args, **kwargs)
        db.close()
        return res
    return wrapper


@db_connect
def create_tables():
    db.create_tables([Meme, User])


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return None, 0
        return cls.select().where(cls.id.in_(ids)), total

    @classmethod
    def update_index(cls, obj):
        add_to_index(obj.__tablename__, obj)

    @classmethod
    def remove_index(cls, obj):
        remove_from_index(obj.__tablename__, obj)

    @classmethod
    @db_connect
    def reindex(cls):
        for obj in cls.select():
            add_to_index(obj.__tablename__, obj)


class Meme(Model, SearchableMixin):
    __searchable__ = ['mem_text']
    __tablename__ = 'meme'
    mem_id = CharField(unique=True)
    mem_text = TextField(null=True)
    mem_category = CharField(null=True)
    date_added = DateField(default=datetime.date.today())

    @classmethod
    @db_connect
    def insert_mem(cls, photo_mem_id, text_mem):
        if cls.get_or_none(cls.mem_id == photo_mem_id) is None:
            obj = cls.create(
                mem_id=photo_mem_id,
                mem_text=text_mem
            )
            cls.update_index(obj)

    @classmethod
    @db_connect
    def get_mem_id_or_none(cls, photo_mem_id):
        return cls.get_or_none(cls.mem_id == photo_mem_id)

    @classmethod
    @db_connect
    def get_mem_or_none(cls, text_search):
        mem, total = cls.search(text_search, 1, 10)
        return [(i.mem_id, i.mem_text) for i in mem]

    @classmethod
    @db_connect
    def mem_count(cls):
        return cls.select().count()

    @classmethod
    @db_connect
    def get_all(cls):
        res = cls.select()
        for i in res:
            print(i.mem_text)

    class Meta:
        database = db


class User(Model):
    user_id = CharField(unique=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    language_code = CharField(null=True)
    connection_date = DateField()

    @classmethod
    @db_connect
    def user_update(cls, message: Message):
        if cls.get_or_none(cls.user_id == message.from_user.id) is None:
            new_user = cls.create(
                user_id=message.from_user.id,
                username=message.from_user.username,
                connection_date=datetime.date.today()
            )
            if message.from_user.first_name:
                new_user.first_name = message.from_user.first_name
                new_user.save()
            if message.from_user.last_name:
                new_user.last_name = message.from_user.last_name
                new_user.save()
        else:
            user = cls.select().where(cls.user_id == message.from_user.id).first()
            if user.connection_date == datetime.date.today():
                return
            user.connection_date = datetime.date.today()
            user.save()

    @classmethod
    @db_connect
    def user_count(cls):
        return cls.select().count()

    class Meta:
        database = db
