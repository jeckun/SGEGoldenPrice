# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trader'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return "<Trade(name='%s')>" % self.name
