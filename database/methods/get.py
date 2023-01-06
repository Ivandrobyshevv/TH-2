from sqlalchemy import or_
from sqlalchemy.sql.elements import and_

from database.engine import engine
from sqlalchemy.orm import sessionmaker
from database.models import Products

session = sessionmaker(bind=engine)


class GetDataBase:
    @staticmethod
    def get_product_links_all(category=None):
        if category is not None:
            with session() as s:
                list_data = [link[0] for link in s.query(Products.link).filter(Products.category_id == category).all()]
            return list_data
        else:
            with session() as s:
                list_data = [link[0] for link in s.query(Products.link).all()]
            return list_data

    @staticmethod
    def get_is_publish_true(category):
        with session() as s:
            list_data = [link[0] for link in s.query(Products.link).filter(and_(Products.is_published == True,
                                                                                Products.category_id == category)).all()
                         ]
            return list_data

    @staticmethod
    def get_product_url(link):
        with session() as s:
            data = s.query(Products).filter(Products.link == link)
        return data

    @staticmethod
    def get_is_publish_card_none(category=None):
        if category is not None:
            with session() as s:
                list_data = [link[0] for link in s.query(Products.link).filter(
                    and_(Products.is_published == None, Products.category_id == category)).all()]
                return list_data
        else:
            raise ("Введиет категорию!")
