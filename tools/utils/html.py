# -*- coding: UTF-8 -*-
'''
@Project ：spider_kit 
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
import re
from typing import Iterable, Optional, Union
from xml.sax.saxutils import unescape

from parsel import Selector
from w3lib.html import (
    remove_tags_with_content,
    replace_escape_chars,
    strip_html5_whitespace,
    remove_comments as html_remove_comments,
    remove_tags as html_remove_tags,
)


def html_unescape(content):
    '''
    将 content 变为 html 语言
    比如 &nt &gt... 变成<>
    :param content:
    :return:
    '''
    return unescape(content)


def replace_tags(text: str, old_tag, new_tag):
    '''
    将文本中的tag类型替换
    :param text:
    :param old_tag:
    :param new_tag:
    :return:
    '''
    content = re.sub(f"<{old_tag}.*?>", f"<{new_tag}>", text)
    content = re.sub(f"<{old_tag}.*?>", f"<{new_tag}>", content)
    return content


def remove_tags(text: str, which_ones: Iterable[str], keep: Iterable[str] = ()):
    '''
    仅删除 HTML 标签

    which_ones keep 它能做什么
    不是空的 空的 删除所有which_ones标签
    空的 不是空的 删除所有标签keep之外的标签
    空的 空的 删除所有标签
    不是空的 不是空的 不允许

    :param text:
    :param which_ones:
    :param keep:
    :return:
    '''
    return html_remove_tags(text, which_ones, keep)


def remove_tags_content(text: str, which_ones: Iterable[str] = ()):
    '''
    删除标签及其内容
    :param text:HTML
    :param which_ones: 要删除哪些标签的元组， 包括他们的内容
    :return: 如果为空， 则返回未修改的字符串
    '''
    return remove_tags_with_content(text, which_ones)


def remove_comments(text: str):
    '''
    删除HTML注释
    :param text:HTML
    :return:
    '''
    return html_remove_comments(text)


def remove_escape_chars(text: str):
    '''
    删除转义字符
    :param text: HTML
    :return:
    '''
    return replace_escape_chars(text)


def remove_html5_whitespace(text: str):
    '''
    去除所有前后空格字符( \t\n\r\x0c)
    :param text:
    :return:
    '''
    return strip_html5_whitespace(text)


def _remove_content(text, xpath):
    html = Selector(text=text)
    if xpath:
        html.xpath(xpath).drop()
    return html.get()


def html_remove_content_by_xpath(
        text: Union[list[str], str],
        param: Optional[str] = None
):
    '''
    根据xpath来移除html中的内容
    :param text:
    :param params:
    :return:
    '''
    return (
        [_remove_content(t, param) for t in text]
        if isinstance(text, list)
        else _remove_content(text, param)
    )


def html_delete_attrib(
        text: Union[list[str], str],
        param: Optional[str] = "style"
):
    '''
    删除html中指定的属性， 默认为style
    :param text: html文本
    :param param: 属性名
    :return:
    '''

    def _remove_style(html_text: str):
        selector = Selector(text=html_text)
        for element in selector.xpath("//*"):
            element.root.attrib.pop(param, None)
        return selector.get()

    return (
        [_remove_style(t_) for t_ in text]
        if isinstance(text, list)
        else _remove_style(text)
    )


def html_find_specific_string(text: str, params: str = ""):
    """
    使用re.search，正则解析html文本
    :param text: 正则文本
    :param params: 需要替换的字符串
    :return:

    example：
        raw_text = "onclick="window.open('/njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html');"
        new_text = html_find_specific_string(text, "window.open('{}')")
        print(new_text) => /njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html

    """  # noqa: E501
    pattern = "(.*?)".join([re.escape(s) for s in params.split("{}")])
    values = re.search(pattern, text)
    if values and len(values.groups()) == 1:
        return values.group(1)
    elif values and len(values.groups()) > 1:
        return values.groups()
    else:
        return None


def html_replace_tag_content(
        content: str | Selector,
        replace_xpath: str,
        new_text: str
):
    '''
    替换正文中指定xpath标签的内容
    :param content:正文内容
    :param replace_xpath:需要替换内容的xpath位置
    :param new_text:替换的文本内容
    :return:
    '''
    content_html = Selector(text=content) if isinstance(content, str) else content
    content_node = content_html.xpath(replace_xpath)
    for old_content in content_node:
        old_content.root.text = new_text
    new_content = "".join(content_html.extract())
    return new_content


def html_replace_attrib(
        content: str | Selector,
        replace_xpath: str,
        replace_attrib: str,
        new_attrib_value: str
):
    '''
    修改正文中对应xpath的正文内容

    :param content:正文内容
    :param replace_xpath:需要替换内容的xpath位置
    :param replace_attrib:需要替换内容的attrib属性
    :param new_attrib_value:替换的attrib正文内容
    :return:
    '''
    content_html = Selector(text=content) if isinstance(content, str) else content
    content_node = content_html.xpath(replace_xpath)
    for old_content in content_node:
        old_content.root.attrib[replace_attrib] = new_attrib_value
    new_content = "".join(content_html.extract())
    return new_content


def html_search_by_re(
        value: str,
        pattern: str,
        index: int = -1,
        join_str: str = ""
) -> str:
    '''
    从html中，使用re.search， 获取指定xpath解析出的内容
    :param value: html内容
    :param pattern: re表达式
    :param index: 需要获取下标的情况下使用， 默认为-1获取全部
    :param join_str: 获取全部的时候，连接列表的字符， 默认为空字符串
    :return:
    '''
    res = re.findall(pattern, value)
    if index == -1:
        return join_str.join(res)
    else:
        return res[index]


def html_sub_by_re(
        value: str,
        pattern: str,
        new_str: str = ""
) -> str:
    '''
    从html中， 使用re.sub， 获取指定xpath解析出的内容
    :param value: html内容
    :param pattern: re表达式
    :param new_str: 需要替换的新的字符， 默认为""
    :return:
    '''
    return re.sub(pattern, new_str, value)

def html_findall_by_re(
        value: str,
        pattern: str,
        index: int = -1,
        join_str: str = ""
):
    '''
    从html中， 使用re.findall， 获取指定xpath解析出的内容
    :param value: html内容
    :param pattern:  re表达式
    :param index: 需要获取下标的情况下使用，默认为-1获取全部
    :param join_str: 获取全部的时候，连接列表的字符，默认为空字符串
    :return:
    '''
    res = re.findall(pattern, value)
    if index == -1:
        return join_str.join(res)
    else:
        return res[index]

