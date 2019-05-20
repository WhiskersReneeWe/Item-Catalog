#!/usr/bin/env python3

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


########## User ########################
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    username = Column(String(20), server_default = 'DB Admin', nullable = False)
    email = Column(String(120), nullable = False, index = True, unique = True)

    @property
    def serialize(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
               }
########## User ########################


########### Category####################
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
                'name': self.name,
                'Category_id': self.id
               }
########### Category####################


########### Item #######################

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    date_added = Column(DateTime(timezone = True), server_default = func.now())
    date_edited = Column(DateTime(timezone = True), onupdate = func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
                'name': self.name,
                'Item_id': self.id,
                'description': self.description,
                'date_added': self.date_added,
                'date_edited': self.date_edited
               }
########### Item #######################


engine = create_engine('sqlite:///ItemCatalog.db')

Base.metadata.create_all(engine)
