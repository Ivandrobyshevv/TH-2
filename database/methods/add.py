import datetime
import logging
from database.engine import engine
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)


class InsertDataBase:
    @staticmethod
    def add_item(obj):
        with session() as s:
            s.add(obj)
            s.commit()
            logging.info(f"item add in data base {datetime.datetime.now()}")

    @staticmethod
    def add_item_autoincrement(obj):
        with session() as s:
            s.add(obj)
            s.flush()
            s.commit()
            logging.info(f"item add in data base {datetime.datetime.now()}")
