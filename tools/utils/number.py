# -*- coding: UTF-8 -*-
'''
@Project ：spider_kit 
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
from decimal import Decimal

from number_parser import parse_number
from price_parser import Price


def price_parse(price_str) -> "Decimal":
    '''
    解析价格相关的字符串
    :param price_str: "22,90 €"
    :return: Decimal("22,90")
    '''
    price = Price.fromstring(price_str)
    return price.amount


def number_parse(number_str: str) -> int:
    '''
    解析数字相关的字符串
    :param number_str: "two thousand and twenty"
    :return: 2020
    '''
    return parse_number(number_str)
