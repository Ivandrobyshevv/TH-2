from typing import Any

from sqlalchemy import Integer, Column, String, Text, Float, Boolean
from database.engine import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    id_product = Column(String)
    title = Column(String)
    description = Column(Text)
    size = Column(String)  # размеры
    colors = Column(String)  # цвета
    composition = Column(String)  # состав
    img = Column(Text)
    old_price = Column(Float)
    new_price = Column(Float)
    link = Column(Text, unique=True)  # ссылка на продукт в магазине
    category_id = Column(Integer)
    is_published = Column(Boolean)

    def __init__(self, title, old_price, new_price, img, link, category_id):
        self.title = title
        self.old_price = old_price
        self.new_price = new_price
        self.img = img
        self.link = link
        self.category_id = category_id

    def __str__(self):
        return f"Object <{id(self)} / {self.title}>"
