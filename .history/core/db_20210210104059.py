# -*- coding: utf-8 -*-
import sqlite3
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime

from config import DB_PATH

Base = declarative_base()


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


class TimeSharingChart(Base):
    __tablename__ = 'timeSharing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trans_date = Column(DateTime)  # 交易日期
    code = Column(String(20), nullable=False)  # 合约
    price = Column(
        Float(precision=10, decimal_return_scale=2), default=0.00)  # 最新价格
    VWAP = Column(Float(precision=10, decimal_return_scale=2))  # 加权平均价
    spread = Column(Float(precision=10, decimal_return_scale=2))  # 涨跌（元）
    extent = Column(Float(precision=10, decimal_return_scale=6))  # 涨跌幅
    volume = Column(Float(precision=10, decimal_return_scale=2))  # 成交量

    def __repr__(self):
        return "<TimeSharingChart(trans_date='%s' code='%s')>" % (self.trans_date.strftime('%Y-%m-%d'), self.code)


class Trade(Base):
    __tablename__ = 'trader'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trans_date = Column(Date)  # 交易日期
    code = Column(String(20), nullable=False)  # 合约
    open = Column(
        Float(precision=10, decimal_return_scale=2), default=0.00)  # 开盘价
    high = Column(Float(precision=10, decimal_return_scale=2))  # 最高价
    low = Column(Float(precision=10, decimal_return_scale=2))  # 最低价
    close = Column(Float(precision=10, decimal_return_scale=2))  # 收盘价
    spread = Column(Float(precision=10, decimal_return_scale=2))  # 涨跌（元）
    extent = Column(Float(precision=10, decimal_return_scale=6))  # 涨跌幅
    VWAP = Column(Float(precision=10, decimal_return_scale=2))  # 加权平均价
    volume = Column(Float(precision=10, decimal_return_scale=2))  # 成交量
    turnover = Column(Float(precision=10, decimal_return_scale=2))  # 成交金额
    hold = Column(Float(precision=10, decimal_return_scale=2))  # 市场持仓
    settlement = Column(String(20))  # 交收方向
    settlement_volume = Column(
        Float(precision=10, decimal_return_scale=2))  # 交收量

    def __repr__(self):
        return "<Trade(trans_date='%s' code='%s')>" % (self.trans_date.strftime('%Y-%m-%d'), self.code)

    @static
# engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
s = 'sqlite:///' + DB_PATH + '?check_same_thread=False'
engine = create_engine(s, echo=False)
Base.metadata.create_all(engine, checkfirst=True)

se = sessionmaker(bind=engine)
session = se()
