#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///beermenuwithusers.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Print all entries in table catetegory
categories = session.query(Category).order_by(asc(Category.name)).all()
for i in categories:
	print(i)