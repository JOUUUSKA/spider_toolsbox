import random
import time
from fake_useragent import UserAgent


def create_timestamp():
    """
    :return: 时间戳


    此函数用于创建一个在爬虫任务中经常出现的时间戳
    """
    return round(time.time() * 1000)


def create_random_str(length=16, pool=None):
    """
    :param length: 指定需要返回的random_str个数
    :param pool: 指定random_str的pool范围
    :return: random_str


    此函数用于创建一个在爬虫任务中经常出现的 乱序大小写英文字母＋数字 随机字符组合，
    随机字符组合池默认为ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890，可以自行指定，
    随机字符组合位数默认为16位，可以自行指定
    """
    if pool is None:
        pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    result = ""
    for i in range(length):
        result += random.choice(pool)
    return result


def create_headers():
    """
    :return: 随机请求头


    此函数用于创建一个随机，常用的请求头
    """
    return {"User-Agent": UserAgent().random}
