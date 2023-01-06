from sqlalchemy.orm import sessionmaker

from database.engine import engine
from database.models import Products

session = sessionmaker(bind=engine)


class UpdateDataBase:
    @staticmethod
    def update_price(card_link, old_price, new_price):
        with session() as s:
            product = s.query(Products).filter(Products.link == card_link).one()
            product.old_price = old_price
            product.new_price = new_price
            s.add(product)
            s.commit()

    @staticmethod
    def disabled_products(card_link):
        with session() as s:
            product = s.query(Products).filter(Products.link == card_link).one()
            product.is_published = False
            s.add(product)
            s.commit()

    @staticmethod
    def update_items_card(card_link, id_product=None, description=None, colors=None, composition=None, size=None):
        with session() as s:
            product = s.query(Products).filter(Products.link == card_link).one()
            product.is_published = True
            product.id_product = id_product
            product.description = description
            product.colors = colors
            product.composition = composition
            product.size = size
            s.add(product)
            s.commit()
