import os

import requests
import tools


def download_video(url, headers=None, data=None, params=None, name=None, type_=None, mode=None, **kwargs):
    """
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param type_: 下载文件的后缀名，如果没有指定，则默认为mp4
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 视频 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 tools.headers
    type_ 默认为 'mp4'
    name 默认为 str(tools.video_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_video文件夹，对下载的视频进行持久化存储
    """
    if type_ is None:
        type_ = "mp4"
    if name is None:
        name = str(tools.video_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = tools.headers
    if not os.path.exists("./Download_video"):
        os.mkdir("./Download_video")
    response = requests.get(url, headers=headers, data=data, params=params, **kwargs)
    if response.status_code == 200:
        with open(f"./Download_video/{name}.{type_}", mode) as f:
            f.write(response.content)
            print(f"{name}.{type_} 下载成功")
    else:
        print(f"{name}.{type_} 下载失败")


def download_img(url, headers=None, data=None, params=None, name=None, type_=None, mode=None, **kwargs):
    """
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param type_: 下载文件的后缀名，如果没有指定，则默认为jpg
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 图片 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 tools.headers
    type_ 默认为 'jpg'
    name 默认为 str(tools.image_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_image文件夹，对下载的 图片 进行持久化存储
    """
    if type_ is None:
        type_ = "jpg"
    if name is None:
        name = str(tools.image_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = tools.headers
    if not os.path.exists("./Download_img"):
        os.mkdir("./Download_img")
    response = requests.get(url, headers=headers, data=data, params=params, **kwargs)
    if response.status_code == 200:
        with open(f"./Download_img/{name}.{type_}", mode) as f:
            f.write(response.content)
            print(f"{name}.{type_} 下载成功")
    else:
        print(f"{name}.{type_} 下载失败")


def download_character(txt, name=None, type_=None, mode=None):
    """
    :param txt: 需要下载的 文字 或 响应
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param type_: 下载文件的后缀名，如果没有指定，则默认为txt
    :param mode: 下载文件时的模式，如果没有指定，则默认为w
    :return: None


    此函数用于在爬虫任务中，
    通过一个给定的文本，快速地进行 文本 下载操作

    TXT为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    type_ 默认为 'txt'
    name 默认为 str(tools.txt_name())
    mode 默认为 'w'

    并在此文件夹下新建一个Download_txt文件夹，对下载的 文本 进行持久化存储
    """
    if type_ is None:
        type_ = "txt"
    if name is None:
        name = str(tools.txt_name())
    if mode is None:
        mode = "w"
    if not os.path.exists("./Download_txt"):
        os.mkdir("./Download_txt")
    with open(f"./Download_txt/{name}.{type_}", mode) as f:
        f.write(txt)
