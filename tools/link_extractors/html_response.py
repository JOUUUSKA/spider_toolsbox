# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：html_response.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:16 
'''
from typing import List
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.selector import SelectorList
from scrapy.utils.response import get_base_url
from w3lib.html import strip_html5_whitespace
from w3lib.url import safe_url_string

from spider_toolsbox.tools.utils.text import clear_text
from spider_toolsbox.tools.utils.html import html_find_specific_string
from spider_toolsbox.tools.utils.url import is_valid_url

from utils import extract_date

link_attrib = ["href", "src", "url", "data-href", "data-value"]

special_link_attrib = ["onclick"]



text_xpath = ["./@title", "string(.)", "./text()", "./@value"]


def _iter_links(selector_list: List[Selector]):
    """
    从选择器列表中提取链接

    :param selector_list: 选择器列表
    :return:
    """
    for sel in selector_list:
        attribs = sel.attrib
        for attrib in attribs:
            if attrib not in link_attrib:
                continue
            else:
                yield sel, attrib, attribs[attrib]


def _iter_special_links(selector_list: List[Selector]):
    """
    从特殊的选择器列表中提取链接

    :param selector_list: 特殊的选择器列表
    :return:
    """
    for sel in selector_list:
        attribs = sel.attrib
        for attrib in attribs:
            if attrib not in special_link_attrib:
                continue
            else:
                yield sel, attrib, attribs[attrib]


def _iter_text(selector_list: List[Selector]):
    """
    从选择器列表中提取文本

    :param selector_list: 选择器列表
    :return:
    """
    for sel in selector_list:
        for xpath in text_xpath:
            text = sel.xpath(xpath).get()
            if not text:
                continue
            else:
                yield text
                break


def _extract_text(selector: SelectorList):
    """
    从选择器列表中提取文本

    :param selector: 选择器列表
    :return:
    """
    text_list = []
    for text in _iter_text(selector):
        text = clear_text(text)
        text_list.append(text.strip())
    return text_list


def _extract_links(
    selector: SelectorList, response_url: str, response_encoding: str, base_url: str
):
    """
    从选择器列表中提取链接

    :param selector: 选择器列表
    :param response_url: response url
    :param response_encoding:  response encoding
    :param base_url: 网站域名，提取到的链接是相对路径时，需要拼接
    :return:
    """
    urls = []
    for _el, _attr, attr_val in _iter_links(selector):
        attr_val = strip_html5_whitespace(attr_val)
        attr_val = urljoin(base_url, attr_val)

        url = attr_val

        if not is_valid_url(url):
            continue
        url = safe_url_string(url, encoding=response_encoding)
        # to fix relative links after process_value
        url = urljoin(response_url, url)

        urls.append(url)

    for _el, _attr, attr_val in _iter_special_links(selector):
        attr_val = strip_html5_whitespace(attr_val)
        url = attr_val

        if not url:
            continue

        filterd_urls = filter_urls(url)
        if not filterd_urls:
            continue

        for f_url in filterd_urls:
            url = urljoin(response_url, f_url)

            if not is_valid_url(url):
                continue
            url = safe_url_string(url, encoding=response_encoding)
            # to fix special links after process_value
            urls.append(url)

    return urls


def filter_urls(urls: list | str) -> list:
    """
    从原始的url中提取出正确的url链接

    :param urls 原始的url
        window.open('/njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html');"
        window.open('/njweb/zbjh/20240801/9fc5b186-d2ef-4e41-1234-6f4103df9f52.html','','');"
    :return: 匹配到的url
        /njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html
        /njweb/zbjh/20240801/9fc5b186-d2ef-4e41-1234-6f4103df9f52.html
    """
    clean_attachment_links = []
    if isinstance(urls, str):
        if '(' in urls and ')' in urls:
            element = html_find_specific_string(urls, "('{}')") or html_find_specific_string(urls, '("{}")')
            if element and "," in element:
                element = element.split(",")[0].strip()[:-1]
                clean_attachment_links.append(element)
            elif element:
                clean_attachment_links.append(element)
        else:
            clean_attachment_links.append(urls)
        return clean_attachment_links
    else:
        for att_link in urls:
            clean_attachment_links.extend(filter_urls(att_link))
    return clean_attachment_links


def extract_link_by_response_xpath(response: "HtmlResponse", xpath: str):
    """
    通过xpath从scrapy response中解析链接

    :param response: scrapy response
    :param xpath: xpath
    :return:
    """
    base_url = get_base_url(response)
    return _extract_links(
        response.xpath(xpath), response.url, response.encoding, base_url
    )


def extract_text_by_response_xpath(response: "HtmlResponse", xpath: str):
    """
    通过xpath从scrapy response中解析文本

    :param response: scrapy response
    :param xpath: xpath
    :return:
    """
    elements = response.xpath(xpath)
    return _extract_text(elements)

def extract_date_by_response_xpath(response: "HtmlResponse", xpath: str):
    """
    通过xpath从scrapy response中解析文本

    :param response: scrapy response
    :param xpath: xpath
    :return:
    """
    elements = response.xpath(xpath).get()
    return extract_date(elements)
