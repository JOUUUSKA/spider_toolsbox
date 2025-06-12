# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
import re
from typing import Any
from urllib import parse
from urllib.parse import parse_qs, unquote, urlparse, urlsplit

from w3lib.url import (
    add_or_replace_parameter,
    add_or_replace_parameters,
    canonicalize_url,
)

from tools.constants.constants import EXT_TYPES


def is_attachment_href(href: str) -> bool:
    '''
    判断链接是否含有附件

    :param href: 字符串链接 <a href="xxxx">name.pdf</a>
    :return: True or False
    '''
    if not href:
        return False
    for ext in EXT_TYPES:
        if ext in href:
            return True
    return False


def url_encode(url: str, safe_word: str = "/") -> str:
    '''
    字符串 url 编码
    :param url: "你好"
    :param safe_word:
    :return: "%E4%BD%A0%E5%A5%BD"
    '''
    return parse.quote(url, safe=safe_word)


def url_decode(url: str) -> str:
    '''
    字符串 url解码
    :param url: "%E4%BD%A0%E5%A5%BD"
    :return: "你好"
    '''
    return parse.unquote(url)


def url_query_encode(query: dict[str, Any]) -> str:
    '''
    对params 的字典 进行url编码
    :param query: {"wd": "python3标准库"}
    :return: "wd=python3%E6%A0%87%E5%87%86%E5%BA%93"
    '''
    return parse.urlencode(query)


def url_query_to_dict(url: str) -> dict[str, Any]:
    '''
    将url后的参数提取出来生成字典
    :param url: https://www.xxx.com?a=2&c=3
    :return: {"a":"2", "c":"3"}
    '''
    ret_dict = {}
    querys = parse.urlparse(url).query
    if querys:
        for query in querys.split("&"):
            key, value = query.split("=")
            ret_dict[key] = value
    return ret_dict


def clear_url(url: str) -> str:
    '''
    对正则匹配后的 a标签的href进行清洗
    :param url: ' "http://xxxx.xxxx.xxxx" target=_blank'
    :return: 'http://xxxx.xxxx.xxxx'
    '''
    return url.replace('"', "").replace(" ", "").replace("target=_blank", "")


def add_or_replace_param(url: str, param_key: str, param_value: str) -> str:
    '''
    新增或替换url中的单个参数

    :param url: http://xxxx.example.com/index.php
    :param param_key: arg
    :param param_value: value
    :return: http://xxxx.example.com/index.php?arg=value
    '''
    return add_or_replace_parameter(url, param_key, param_value)


def add_or_replace_params(url: str, params: dict[str, Any]) -> str:
    '''
    新增或替换url中的多个参数

    :param url: http://xxxx.example.com/index.php
    :param param_key: {"arg": "value"}
    :return: http://xxxx.example.com/index.php?arg=value
    '''
    return add_or_replace_parameters(url, params)


def format_url(url: str) -> str:
    '''
    格式化url
    url编码， 使url安全，
    对查询参数进行排序， 先按键，后按值
    对所有空格(在查询参数中) "+" (加号)规范化
    将百分比编码的大小写规范化 (%2f -> %2F)
    删除有空白值的查询参数
    :param url: http://xxxx.example.com/r\u00e9sum\u00e9
    :return: http://xxxx.example.com/r%C3%A9sum%C3%A9
    '''
    return canonicalize_url(url)


def parse_params(url: str) -> dict[str, Any]:
    '''
    解析出url的后缀生成字典

    :param url: "http://xxx?a=1&b=2"
    :return: {"a":"['1']", "b":"['2']"}
    '''
    return parse_qs(urlparse(url).query)


def get_url_path(url: str):
    '''
    删除url的后缀， 取出path
    :param url: "http://xxx?a=1&b=2"
    :return: http://xxx
    '''
    return urlsplit(url)._replace(query=None).geturl()


def is_valid_url(url):
    '''
    判断url是否有效
    :param url:
    :return:
    '''
    if str(url).startswith("http"):
        return True
    else:
        return False


def url_find_file(value: str, del_content: str | None = None) -> str:
    '''
    从url中找到file链接
    :param del_content: 提取到file=后的文件url， 再使用正则取出指定去除的内容
    :param value: "http://abc/file=http://def.pdf&page=1&submit=2"
    :return: "http://def"
    '''
    url = re.search(r"(?:file=|fileUrl=|src=//)(.*)", value)
    if url is not None:
        url_sub = unquote(url.group(1))
        if del_content is not None:
            url_sub = re.sub(del_content, '', url_sub)
        return url_sub
    else:
        return value


def complete_url(url: str, protocol: str) -> str:
    '''
    补全url
    :param url: "xxxx.example.com/index.php"
    :param protocol: "https://"
    :return: "http://xxxx.example.com/index.php"
    '''
    protocol = "https://" if not protocol else protocol
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = urlparse(f"{protocol}{url}")
    parsed_protocol = urlparse(protocol)

    scheme = parsed_protocol.scheme if parsed_protocol.scheme else parsed_url.scheme
    netloc = parsed_protocol.netloc if parsed_protocol.netloc else parsed_url.netloc

    update_url = parsed_url._replace(scheme=scheme, netloc=netloc)

    return update_url.geturl()
