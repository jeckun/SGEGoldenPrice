# -*- coding: utf-8 -*-
import os
import sqlite3
import sqlalchemy
from datetime import datetime
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import sessionmaker

from config import DB_PATH

Base = declarative_base()


class Engine(object):
    def __init__(self):
        pass

    def connect(self, filename=None, echo=True):
        if filename == None and echo == True:
            self.engine = create_engine('sqlite:///:memory:', echo=echo)
        elif filename != None:
            db_path = 'sqlite:///' + os.path.join(DB_PATH, 'data', filename)
            self.engine = create_engine(db_path, echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def insert(self, row):
        self.session.add(row)
        self.session.commit()

    def delete(self, row):
        if type(row) == sqlalchemy.orm.query.Query:
            [self.session.delete(u) for u in row]
        elif type(row) == type(self):
            self.session.delete(row)
        self.session.commit()

    def update(self, row):
        self.session.commit()

    def find(self, **kwargs):
        cmd = "self.session.query(%s)" % self.__class__.__name__
        for kw in kwargs:
            cmd += ".filter(%s.%s == '%s')" % (self.__class__.__name__, kw,
                                               kwargs[kw])
        cmd += ".first()"
        return eval(cmd)

    def filter(self, **kwargs):
        cmd = "self.session.query(%s)" % self.__class__.__name__
        for kw in kwargs:
            cmd += ".filter(%s.%s == '%s')" % (self.__class__.__name__, kw,
                                               kwargs[kw])
        return eval(cmd)

    def query_all(self):
        cmd = "self.session.query(%s).all()" % self.__class__.__name__
        return eval(cmd)


class sqliteEngine(object):
    def __init__(self, filename=None):
        if filename:
            self.conn = sqlite3.connect(filename)
            self.cur = self.conn.cursor()

    def delete_all(self, tablename):
        sql = "delete from %s;" % tablename
        self.cur.execute(sql)
        self.conn.commit()

    def select_all(self, tablename):
        sql = "select * from %s;" % tablename
        rst = self.cur.execute(sql)
        return rst

    def execut_sql(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
