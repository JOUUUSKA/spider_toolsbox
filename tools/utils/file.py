# -*- coding: UTF-8 -*-
'''
@Project ：spider_kit 
@File    ：date.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-07-14 15:23 
'''
import re
from typing import Dict
from urllib.parse import unquote

from tools.constants.constants import EXT_TYPES
from tools.utils.text import decode_bytes

default_file_name = "附件"


def file_add_ext_type(file_url: str, file_name: str) -> tuple[str, str]:
    '''
    判断url, name是否有后缀， 如果name无后缀而URL有后缀， 则将URL后缀添加到name中
    :param file_url:
    :param file_name:
    :return:
    '''
    # 移除url中的参数， 防止参数影响判断
    simple_file_url = file_url.split("?")[0]
    origin_file_name = file_name or default_file_name
    file_name = file_name.strip()
    for ext_type in EXT_TYPES:
        if file_name.lower().endswith(ext_type.lower()):
            return origin_file_name, file_name
        else:
            if simple_file_url.lower().endswith(ext_type.lower()):
                return origin_file_name, f"{file_name}.{ext_type}"
    else:
        return origin_file_name, ""


def has_ext_type(file_name: str) -> bool:
    '''
    判断文件名是否有后缀
    :param file_name:
    :return:
    '''
    for ext_type in EXT_TYPES:
        if file_name.lower().endswith(ext_type.lower()):
            return True
    else:
        return False


def select_valid_filename(*filenames):
    '''
    从多个文件名中选择一个有后缀的文件名
    :param filenames:
    :return:
    '''
    valid_file_name = ""
    for filename in filenames:
        if filename and not valid_file_name:
            valid_file_name = filename
        if has_ext_type(filename):
            valid_file_name = filename
            break
    return valid_file_name


def get_filename_by_headers(headers: Dict[str, bytes]) -> str:
    '''
    输入提取后的response.headers内容
    形如response.headers["Content-Disposition"]
    b"attachment; filename=NMG00014000000479-..."
    key为=号前的内容， 用于正则
    :param headers:
    :return:
    '''
    file_content = headers.get("Content-Disposition", b"")
    file_content = decode_bytes(file_content)
    file_content = unquote(file_content, "utf-8")
    file_type = headers.get("Content-Type", b"")
    file_type = decode_bytes(file_type)

    if search_result := re.search(r"/(\w+)", file_type):
        file_type = search_result.group(1)
    info = re.search('[filename,fileName]="?([^";]+)"?', file_content)
    if info:
        file_name = info.group(1)
    else:
        file_name = default_file_name
    if has_ext_type(file_name):
        return file_name
    elif file_type:
        return f"{file_name}.{file_type}"
    else:
        return file_name
