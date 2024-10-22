# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
import re
from datetime import date as date_
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import dateparser
from dateparser import parse

from spider_toolsbox.tools.constants.constants import TIME_ZONE

default_value = ""
# 定义中文数字和时间单位的翻译映射表
chinese_translation_map = {
    "零": "0",
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "七": "7",
    "八": "8",
    "九": "9",
    "年": "-",
    "月": "-",
    "日": " ",
    "号": " ",
    "时": ":",
    "分": ":",
    "：": ":",
    "秒": " ",
}
datetime_pattern = (
    r"(?P<date>\d{4}[_ /.-]+\d{1,2}[_ /.-]+\d{1,2})(\D*)("
    r"?P<time>\d{1,2}[ :]+\d{1,2}[ :]*\d{0,2})?"
)


def current_date(format_time: bool = True) -> str | datetime:
    '''
    获取当前日期
    :param format_time:是否格式化
    :return:
    '''
    now = datetime.now()
    return now.strftime("%Y-%m-%d") if format_time else now


def current_datetime(format_time: bool = True) -> str | datetime:
    '''
    获取当前日期
    :param format_time:是否格式化
    :return:
    '''
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S") if format_time else now


def current_timestamp_10() -> int:
    '''
    获取当前10位时间戳
    :return:
    '''
    return int(datetime.now().timestamp())


def current_timestamp_13(fix_last: bool = False) -> int:
    '''
    获取当前13位时间戳
    :param fix_last: 是否固定最后三位为000
    :return:
    '''
    now_t = datetime.now().timestamp()
    if fix_last:
        return int(f"{int(now_t)}000")
    return int(now_t * 1000)


def timestamp_to_datetime(timestamp: int, format_time: bool = True) -> str | datetime:
    '''
    时间戳转换为日期
    :param timestamp:时间戳
    :param format_time:是否格式化
    :return:
    '''
    dt = datetime.fromtimestamp(timestamp, ZoneInfo(TIME_ZONE))
    return dt.strftime("%Y-%m-%d %H:%M:%S") if format_time else dt


def timestamp_to_date(timestamp: int, format_time: bool = True) -> str | date_:
    '''
    时间戳转换为日期
    :param timestamp:时间戳
    :param format_time:是否格式化
    :return:
    '''
    dt = datetime.fromtimestamp(timestamp, ZoneInfo(TIME_ZONE)).date()
    return dt.strftime("%Y-%m-%d") if format_time else dt


def datetime_to_timestamp(dt: str) -> int:
    '''
    日期转换为时间戳
    :param dt: 日期
    :return:
    '''
    return int(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp())


def format_date(dt: str, output_format: str) -> str:
    '''
    格式化日期
    :param dt:日期
    :param output_format:输出格式
    :return:
    '''
    parsed_date = parse(dt)
    if parsed_date is not None:
        return parsed_date.strftime(output_format)
    else:
        return dt


def previous_date(day_nums: int = 0, date_model: str = "%Y-%m-%d") -> str:
    '''
    输入数字返回距离当天第X天的日期， 年-月-日 日期为该天00:00:00 默认为当天
    date_model 可以设置日期格式 默认为年-月-日 如2001-01-31
    :param day_nums:
    :param date_model:
    :return:
    '''
    today = date_.today()
    previous_day = today - timedelta(days=int(day_nums))
    previous_day = previous_day.strftime(date_model)
    return previous_day


def fallback_date_parser(text: str) -> str:
    '''
    使用 dateparser 解析日期时间字符串， 并将其转换为 ISO 8601 格式
    :param text:携带时间的字符串
    :return:
    '''
    formatted_datetime = dateparser.parse(text, settings={'TIMEZONE': TIME_ZONE})
    if formatted_datetime:
        return formatted_datetime.replace(tzinfo=None).isoformat()

    # 如果解析失败， 则返回默认值
    return default_value


def extract_date(text: str) -> str:
    '''
    提取字符串中的时间
    :param text:携带时间的字符串
    :return:
    '''
    match = re.search(r"\b\d{10}(?:\d{3})?\b", text)
    if match:
        timestamp_str = match.group()[:10]
        formatted_datetime = dateparser.parse(timestamp_str, settings={'TIMEZONE': TIME_ZONE})

        return formatted_datetime.isoformat() if formatted_datetime else ""

    # 将中文数字和时间单位翻译为阿拉伯数字和英文时间单位
    translated_text = translate_chinese(text)

    searched = re.search(datetime_pattern, translated_text)
    if not searched:
        return fallback_date_parser(text)

    date_value, time_value = searched.group("date"), searched.group("time")

    formatted_datetime = parse_datetime(date_value, time_value)
    if formatted_datetime:
        return formatted_datetime.isoformat()

    return fallback_date_parser(text)


def translate_chinese(text: str) -> str:
    '''
    将中文数字和时间单位翻译为阿拉伯数字和英文时间单位
    :param text:携带时间的字符串
    :return:
    '''
    translated_text = "".join(chinese_translation_map.get(char, char) for char in text)
    for matched in re.finditer(r"(?P<tens>\d)?十(?P<ones>\d)?", translated_text):
        number = 10 * (int(matched.group('tens') or 1)) + int(matched.group('ones') or 0)
        translated_text = translated_text.replace(matched.group(), str(number))

    return translated_text


def parse_datetime(date_value: str, time_value: str):
    '''
    使用dateparser 解析日期时间字符串
    :param date_value:日期字符串
    :param time_value:时分秒字符串
    :return:
    '''
    if date_value and time_value:
        formatted_datetime = dateparser.parse(f"{date_value} {time_value}")
        return formatted_datetime if formatted_datetime else ""
    else:
        formatted_datetime = dateparser.parse(date_value)
        return formatted_datetime.date() if formatted_datetime else ""
