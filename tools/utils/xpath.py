# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
from lxml import etree
from loguru import logger
from spider_toolsbox.tools.utils.html import html_find_specific_string  # type: ignore

TEXT_ATTRIBUTE_LIST = ["string(.)", "./text()", "./@title"]
URL_ATTRIBUTE_LIST = ["./@href", "./@src", "./@data-href", "./@onclick", "./@id"]


def xpath_getall(selector_html, attribute):
    """
    根据xpath路径与需要抓取的属性获取内容列表
    :param selector_html:
    :param xpath:
    :param attribute:
    :return:
    """
    info_list = selector_html.xpath(attribute).getall()
    return info_list


def get_xpath_text_info(selector_html, xpath):
    """
    获取xpath中的text列表

    :param selector_html: html
    :param xpath: xpath路径
    :return: text_list
    """
    text_list = []
    if xpath.strip():
        selector_html = selector_html.xpath(xpath)
        for attribute in TEXT_ATTRIBUTE_LIST:
            new_text_list = xpath_getall(selector_html, attribute)
            text_list_join = "".join(new_text_list).strip()
            if text_list_join:
                text_list = new_text_list
                # 如果出现...先检查一轮，如果没有解决则返回带...的内容 解决了就返回没有的内容
                if "..." in text_list_join:
                    continue
                else:
                    break
    return text_list


def get_xpath_url_info(selector_html, xpath):
    """
    获取xpath中的url列表

    :param selector_html: html
    :param xpath: xpath路径
    :return: url_list
    """
    url_list = []
    if xpath.strip():
        selector_html = selector_html.xpath(xpath)
        for attribute in URL_ATTRIBUTE_LIST:
            new_url_list = xpath_getall(selector_html, attribute)
            url_list_join = "".join(new_url_list).strip()
            if url_list_join:
                url_list = new_url_list
                # 如果内容为javascript 大概真实值在onclick等属性中 需要后续特殊处理
                if "javascript:" in url_list_join:
                    continue
                else:
                    break

    return filter_urls(url_list)


def filter_urls(urls: list):
    clean_attachment_links = []
    for att_link in urls:
        if '(' in att_link and ')' in att_link:
            element = html_find_specific_string(att_link, "('{}')") or html_find_specific_string(att_link, '("{}")')
            if element and "," in element:
                element = element.split(",")[0].strip()[:-1]
                clean_attachment_links.append(element)
            elif element:
                clean_attachment_links.append(element)
        else:
            clean_attachment_links.append(att_link)
    return clean_attachment_links


def get_xpath_content_info(selector_html, xpath):
    """
    获取xpath中的content内容

    :param selector_html: html
    :param xpath: xpath路径
    :return: content
    """
    content = ""
    if xpath.strip():
        news_content = selector_html.xpath(xpath).extract()
        content = "".join(news_content).strip()
    return content


def get_xpath_file_info(selector_html, file_xpath):
    """
    获取xpath中的filename和fileurl列表

    :param selector_html: html
    :param file_xpath: xpath路径
    :return: attachment_names, attachment_links
    """
    attachment_names = []
    attachment_links = []
    if file_xpath and file_xpath.strip() and selector_html:
        attachment_names = get_xpath_text_info(selector_html, file_xpath)
        attachment_links = get_xpath_url_info(selector_html, file_xpath)
    if len(attachment_links) > len(attachment_names):
        logger.warning("附件链接与附件名数量不一致 缺少附件名")
        for i in range(len(attachment_links) - len(attachment_names)):
            attachment_names.append(f"附件{i}")
    return attachment_names, filter_urls(attachment_links)


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
