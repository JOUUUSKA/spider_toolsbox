import random
import time

from fake_useragent import UserAgent
from constants.constants import DEFAULT_USER_AGENT

ua_pool = UserAgent()

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
    return {"User-Agent": ua_pool.random}


def create_default_headers():
    """
    :return: 固定返回一个相同的web端的请求头


    因为create_headers创建的请求头是使用random随机创建，所以可能是移动端的请求头
    这可能导致服务器返回 移动端 的网页结构， 而非 web端 的网页结构
    移动端和web端的页面xpath结构可能不一致，导致xpath锁定不了页面元素
    所以可以使用create_default_headers方法，固定返回一个相同的web端的请求头

    并且使用fakeua库之后，打包出来的exe文件体积会比较大，
    所以如果请求头校验不是很严格，建议使用create_default_headers
    """
    return {"User-Agent": DEFAULT_USER_AGENT}
