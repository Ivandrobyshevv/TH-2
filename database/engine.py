from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine("sqlite:///main.db", echo=True)
Base = declarative_base()