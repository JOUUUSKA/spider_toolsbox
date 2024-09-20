# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''


def page_number(
        start_page: int,
        step: int,
        return_start: int
) -> str:
    '''
    基础的累加翻页函数

    :param start_page: 起始页索引位置， 默认为1
    :param step: 步长，默认为1
    :param return_start: 是否返回的起始页索引位置， 1: 返回， 0: 不返回
    :return: 下一个索引位置
    '''
    if int(return_start):
        next_page = start_page
    else:
        next_page = int(start_page) + int(step)
    return str(next_page)
