# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Numeric, Integer, String, Text, Date, DateTime

from config import DB_PATH

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trader'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trans_date = Column(Date)  # 交易日期
    code = Column(String(20), nullable=False)  # 合约
    open_price = Column(Numeric(10, 2), default=0.00)  # 开盘价
    high_price = Column(Numeric(10, 2))  # 最高价
    low_price = Column(Numeric(10, 2))  # 最低价
    close_price = Column(Numeric(10, 2))  # 收盘价
    spread = Column(Numeric(10, 2))  # 涨跌（元）
    extent = Column(Numeric(10, 6))  # 涨跌幅
    VWAP = Column(Numeric(10, 2))  # 加权平均价
    volume = Column(Numeric(10, 2))  # 成交量
    turnover = Column(Numeric(10, 2))  # 成交金额
    hold = Column(Numeric(10, 2))  # 市场持仓
    settlement = Column(String(20))  # 交收方向
    settlement_volume = Column(Numeric(10, 2))  # 交收量

    def __repr__(self):
        return "<Trade(trans_date='%s' code='%s')>" % (self.trans_date.strftime('%Y-%m-%d'), self.code)


# engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
s = 'sqlite:///' + DB_PATH + '?check_same_thread=False'
engine = create_engine(s, echo=False)
Base.metadata.create_all(engine, checkfirst=True)

se = sessionmaker(bind=engine)
session = se()
