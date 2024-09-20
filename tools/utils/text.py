# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
import re
from pathlib import Path
from typing import List


def decode_bytes(content: bytes, encoding: str = "utf-8") -> str:
    '''
    将bytes类型的内容转换为str
    :param content:
    :param encoding:
    :return:
    '''
    try:
        if isinstance(content, str):
            return content
        return content.decode(encoding)
    except UnicodeDecodeError:
        return content.decode("gbk")


def clear_text(text: str) -> str:
    '''
    清洗特殊字符
    :param text:正文内容
    :return: 清洗后的正文内容
    '''
    re_pattern = '<span .*?>|<!D.*dtd">|\\n|\\t|\\r|\xa0|\\u3000|textarea|&quot;|&lt;'
    return re.sub(re_pattern, '', text)


def tailless_text(text: str) -> str:
    '''
    去除字符串末尾的"类型标注"
    Example:
    tailless('/a/b/c.docs') # => '/a/b/c'

    :param text:需要处理的字符串
    :return: 处理后的字符串
    '''
    return str(Path(text).with_suffix(""))


def clear_title(title: str) -> str:
    '''
    清洗标题
    :param title:
    :return:
    '''
    title = clear_text(title)
    re_pattern = (
        r"[\u003ec\u003e\u0001\u2002\u2003\u0001\uf096\u200c\u200f"
        r"\u202a\u202b\u202c\u2028\ue101\ufeff\ue862\ue861\u200d"
        r"\u200b\u2005\u2006\u2009\ue234\ue0e5\ue261\ue306\ue495"
        r"\ue236\ue0cf\ue0e9\ue00f\ue495\uf0b7\ue00c\ue2e5\ue3ac"
        r"\ue004\ue003\xa0\xad\x96\x7f\u3000|nbsp;"
    )
    title = re.sub(re_pattern, ' ', title)
    return title.strip()


def clear_file_name(file_name: str) -> str:
    '''
    清洗文件名
    :param file_name:
    :return:
    '''
    return clear_text(file_name)


def replace_text(
        value: str | List[str],
        old_re_pattern: str,
        new_text: str

) -> str | List[str]:
    '''
    将传入的 value 中的 old_text 替换成 new_text
    :param value:
    :param old_re_pattern:
    :param new_text:
    :return:
    '''
    if isinstance(value, str):
        return re.sub(old_re_pattern, new_text, value)
    else:
        return [replace_text(v, old_re_pattern, new_text) for v in value]


def remove_text(
        value: str | List[str],
        re_pattern: str,
) -> str | List[str]:
    '''
    将传入的value中的 re_pattern匹配到的内容 删除
    :param value:
    :param re_pattern:
    :return:
    '''
    if isinstance(value, str):
        return re.sub(re_pattern, "", value)
    else:
        return [remove_text(v, re_pattern) for v in value]
