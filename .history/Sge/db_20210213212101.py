# -*- coding: utf-8 -*-

from lib.db import Base, Engine, sqliteEngine, Column, Integer, Float, String, Text, Date, DateTime


class TimeSharingChart(Base, Engine):
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


class Trade(Base, Engine):
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
