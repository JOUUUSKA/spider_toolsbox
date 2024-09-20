# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
from lxml import etree


def is_valid_xpath(xpath_string: str) -> bool:
    '''
    判断xpath是否合法
    :param xpath_string:
    :return:
    '''
    try:
        etree.XPath(xpath_string)
        return True
    except etree.XMLSyntaxError:
        return False
