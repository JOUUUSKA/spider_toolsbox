import os

import tools
from link_extractors.html_response import extract_text_by_response_xpath
from utils.url import is_attachment_href


def download_video(
        url,
        method="get",
        headers=None,
        data=None,
        params=None,
        name=None,
        file_type=None,
        mode=None,
        file_path=None,
        file_name=None,
        **kwargs
):
    """
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为mp4
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 视频 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 tools.headers
    file_type 默认为 'mp4'
    name 默认为 str(tools.video_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_video文件夹，对下载的视频进行持久化存储
    """
    if file_type is None:
        file_type = "mp4"
    if name is None:
        name = str(tools.video_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = tools.create_headers()
    if file_name is None:
        file_name = tools.video_name()
    response = tools.Request(
        url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    if response.status_code == 200:
        if file_path is None:
            with open(f"./{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        else:
            with open(f"{file_path}/{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        tools.success(f"{file_name}.{file_type} 下载成功")
    else:
        tools.critical(f"{name}.{file_type} 下载失败")


def download_file(
        file_url,
        file_name,
        file_type,
        method="get",
        headers=None,
        data=None,
        params=None,
        name=None,
        mode=None,
        file_path=None,
        **kwargs
):
    """
    :param file_url: 需要下载的附件url
    :param file_name: 需要下载的附件name
    :param method: 请求方式
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为mp4
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 视频 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 tools.headers
    file_type 默认为 'mp4'
    name 默认为 str(tools.video_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_file文件夹，对下载的视频进行持久化存储
    """
    if is_attachment_href(file_url):
        checked_file_url = file_url
    else:
        raise ValueError("Invalid file url")

    if name is None:
        name = str(tools.video_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = tools.create_headers()
    response = tools.Request(
        checked_file_url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    if response.status_code == 200:
        if file_path is None:
            with open(f"./{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        else:
            with open(f"{file_path}/{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        tools.success(f"{file_name}.{file_type} 下载成功")
    else:
        tools.critical(f"{name}.{file_type} 下载失败")


def download_img(
        url,
        method="get",
        headers=None,
        data=None,
        params=None,
        name=None,
        file_type=None,
        mode=None,
        file_path=None,
        file_name=None,
        **kwargs
):
    """
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为jpg
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 图片 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 tools.headers
    file_type 默认为 'jpg'
    name 默认为 str(tools.image_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_image文件夹，对下载的 图片 进行持久化存储
    """
    if file_type is None:
        file_type = "jpg"
    if name is None:
        name = str(tools.image_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = tools.create_headers()
    response = tools.Request(
        url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    if response.status_code == 200:
        if file_path is None:
            with open(f"./{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        else:
            with open(f"{file_path}/{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        tools.success(f"{file_name}.{file_type} 下载成功")
    else:
        tools.critical(f"{name}.{file_type} 下载失败")


def download_character_by_response_xpath(
        url,
        xpath,
        method="get",
        headers=None,
        data=None,
        params=None,
        file_name=None,
        file_type=None,
        file_path=None,
        mode=None,
        **kwargs
):
    """
    :param txt: 需要下载的 文字 或 响应
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为txt
    :param mode: 下载文件时的模式，如果没有指定，则默认为w
    :return: None


    此函数用于在爬虫任务中，
    通过一个给定的文本，快速地进行 文本 下载操作

    TXT为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    file_type 默认为 'txt'
    name 默认为 str(tools.txt_name())
    mode 默认为 'w'

    并在此文件夹下新建一个Download_txt文件夹，对下载的 文本 进行持久化存储
    """
    if file_type is None:
        file_type = "txt"
    if file_name is None:
        file_name = str(tools.txt_name())
    if mode is None:
        mode = "w"
    req = tools.Request(
        url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    text = extract_text_by_response_xpath(req, xpath)  # type: ignore

    if file_path is None:
        with open(f"./{file_name}.{file_type}", mode) as f:
            f.write(text)  # type:ignore
    else:
        with open(f"{file_path}/{file_name}.{file_type}", mode) as f:
            f.write(text)  # type:ignore
    tools.success(f"{file_name}.{file_type} 下载成功")


def download_others(
        others,
        name=None,
        file_type=None,
        mode=None,
        file_path=None,
        **kwargs
):
    '''
    为下载其他数据提供一个简洁的api

    :param others: 需要下载的 数据
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为txt
    :param mode: 下载文件时的模式，如果没有指定，则默认为w
    :return: None
    '''
    if file_type is None:
        file_type = "txt"
    if name is None:
        name = str(tools.txt_name())
    if mode is None:
        mode = "w"
    if file_path is None:
        with open(f"./{name}.{file_type}", mode) as f:
            f.write(text)  # type:ignore
    else:
        with open(f"{file_path}/{name}.{file_type}", mode) as f:
            f.write(others)  # type:ignore
    tools.success(f"{name}.{file_type} 下载成功")
