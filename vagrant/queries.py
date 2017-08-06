#!/usr/bin/env python3

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///beermenuwithusers.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Print all entries in table Catetegory
categories = session.query(Category).order_by(asc(Category.name)).all()
for i in categories:
	print(i.name, i.id, i.user_id)

# Print all entries in table User
users = session.query(User).all()
for i in users:
	print(i.name, i.id, i.email) #i.picture

# Print all entries in table Item
items = session.query(Item).all()
for i in items:
	print(i.name, i.id, i.user_id) #i.description