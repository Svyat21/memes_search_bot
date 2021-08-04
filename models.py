from config import db
from peewee import Model, CharField, DateField
import datetime


def db_connect(func):
    def wrapper(*args, **kwargs):
        db.connect()
        res = func(*args, **kwargs)
        db.close()
        return res
    return wrapper


@db_connect
def create_tables():
    db.create_tables([Meme])


class DatabaseUpdater():
    @classmethod
    @db_connect
    def insert_mem(cls, photo_mem_id, text_mem):
        if cls.get_or_none(cls.mem_id == photo_mem_id) is None:
            cls.create(
                mem_id=photo_mem_id,
                mem_text=text_mem
            )

    # @classmethod
    # @db_connect
    # def insert_text_mem(cls, photo_mem_id, text_mem):
    #     mem = cls.get_or_none(cls.mem_id == photo_mem_id)
    #     if mem:
    #         mem.mem_text = text_mem
    #         mem.save()
    #     else:
    #         cls.create(mem_id=photo_mem_id, mem_text=text_mem)

    @classmethod
    @db_connect
    def get_mem_or_none(cls, text_search):
        mem = cls.select().where(cls.mem_text.contains(text_search.lower()))
        return [(i.mem_id, i.mem_text) for i in mem]

    @classmethod
    @db_connect
    def get_all(cls):
        res = cls.select()
        for i in res:
            print(i.mem_text)


class Meme(Model, DatabaseUpdater):
    mem_id = CharField(unique=True)
    mem_text = CharField(null=True)
    mem_category = CharField(null=True)
    date_added = DateField(default=datetime.date.today())

    class Meta:
        database = db
