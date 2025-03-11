import os
from urllib.parse import urljoin

from spider_toolsbox.tools.link_extractors.html_response import (
    extract_text_by_response_xpath,
    extract_link_by_response_xpath
)
from spider_toolsbox.tools.log import success, critical
from spider_toolsbox.tools.other_tools.name import video_name, image_name, txt_name
from spider_toolsbox.tools.other_tools.name import file_name as download_file_name
from spider_toolsbox.tools.request import create_default_headers, create_request
from spider_toolsbox.tools.utils.url import is_attachment_href, is_valid_url


class DownloadError(Exception):
    """自定义下载异常"""
    pass


def save_response_content(
        response,
        file_name=None,
        file_type=None,
        file_path=None,
        mode=None,
):
    if response.status_code == 200:
        if file_path is None:
            with open(fr"./{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        else:
            with open(fr"{file_path}/{file_name}.{file_type}", mode) as f:
                f.write(response.content)  # type:ignore
        success(f"{file_name}.{file_type} 下载成功")
    else:
        critical(f"{file_name}.{file_type} 下载失败")


def download_video(
        url,
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
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param file_name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为mp4
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 视频 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 headers
    file_type 默认为 'mp4'
    file_name 默认为 str(video_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_video文件夹，对下载的视频进行持久化存储
    """
    if file_type is None:
        file_type = "mp4"
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = create_default_headers()
    if file_name is None:
        file_name = str(video_name())
    response = create_request(
        url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    save_response_content(
        response,
        file_name,
        file_type,
        file_path,
        mode,
    )


def download_m3u8(
        m3u8_url: str,
        output_name: str = "output",
        file_path: str = None,
        max_workers: int = 8,
        **kwargs
) -> str:
    """
    M3U8流媒体下载器
    :param m3u8_url: m3u8索引文件地址
    :param output_name: 输出文件名（不含后缀）
    :param file_path: 存储路径
    :param max_workers: 最大并发线程数
    :return: 合并后的文件路径
    """
    from concurrent.futures import ThreadPoolExecutor

    # 获取m3u8内容
    response = create_request(m3u8_url, **kwargs)
    if response.status_code != 200:
        raise DownloadError(f"无法获取M3U8文件，状态码：{response.status_code}")

    # 解析TS列表
    ts_list = [
        urljoin(m3u8_url, line.strip())
        for line in response.text.split("\n")
        if line.strip() and not line.startswith("#")
    ]

    # 下载所有TS片段
    file_path = file_path or os.getcwd()
    ts_dir = os.path.join(file_path, "ts_temp")
    os.makedirs(ts_dir, exist_ok=True)

    def _download_ts(ts_url: str, index: int):
        ts_path = os.path.join(ts_dir, f"seg_{index:04d}.ts")
        with create_request(ts_url, stream=True, **kwargs) as r:
            with open(ts_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        return ts_path

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_download_ts, url, idx)
            for idx, url in enumerate(ts_list)
        ]
        for future in futures:
            future.result()

    # 合并TS文件
    output_path = os.path.join(file_path, f"{output_name}.mp4")
    with open(output_path, "wb") as out_f:
        for idx in range(len(ts_list)):
            seg_path = os.path.join(ts_dir, f"seg_{idx:04d}.ts")
            with open(seg_path, "rb") as in_f:
                out_f.write(in_f.read())
            os.remove(seg_path)

    os.rmdir(ts_dir)
    success(f"M3U8文件合并完成：{output_path}")
    return output_path


def download_file(
        file_url,
        file_type,
        file_name=None,
        method="get",
        headers=None,
        data=None,
        params=None,
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
    headers 默认为 headers
    file_type 默认为 'mp4'
    name 默认为 str(video_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_file文件夹，对下载的文件进行持久化存储
    """
    if is_attachment_href(file_url) or is_valid_url(file_url):
        checked_file_url = file_url
    else:
        raise ValueError("Invalid file url")

    if file_name is None:
        file_name = str(download_file_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = create_default_headers()
    response = create_request(
        checked_file_url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    save_response_content(
        response,
        file_name,
        file_type,
        file_path,
        mode,
    )


def download_img(
        url,
        method="get",
        headers=None,
        data=None,
        params=None,
        file_name=None,
        file_type=None,
        mode=None,
        file_path=None,
        **kwargs
):
    """
    :param url: 需要下载的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None
    :param file_name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为jpg
    :param mode: 下载文件时的模式，如果没有指定，则默认为wb
    :return:None


    此函数用于在爬虫任务中，
    通过一个给定的URL，快速地进行 图片 下载操作

    URL为必填，其他参数为选填，
    如果:
    对其他参数没有进行特别指定，
    那么:
    headers 默认为 headers
    file_type 默认为 'jpg'
    name 默认为 str(image_name())
    mode 默认为 'wb'

    并在此文件夹下新建一个Download_image文件夹，对下载的 图片 进行持久化存储
    """
    if file_type is None:
        file_type = "jpg"
    if file_name is None:
        file_name = str(image_name())
    if mode is None:
        mode = "wb"
    if headers is None:
        headers = create_default_headers()
    response = create_request(
        url,
        method=method,
        headers=headers,
        data=data,
        params=params,
        **kwargs
    )
    save_response_content(
        response,
        file_name,
        file_type,
        file_path,
        mode,
    )


def download_text(
        text,
        file_name=None,
        file_type=None,
        mode=None,
        file_path=None,
        encoding="utf-8",
        **kwargs
):
    '''
    为下载其他数据提供一个简洁的api

    :param text: 需要下载的 数据
    :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为txt
    :param mode: 下载文件时的模式，如果没有指定，则默认为w
    :return: None
    '''
    if file_type is None:
        file_type = "txt"
    if file_name is None:
        file_name = str(txt_name())
    if mode is None:
        mode = "w"
    if file_path:
        with open(fr"{file_path}/{file_name}.{file_type}", mode, encoding=encoding) as f:
            f.write(text)  # type:ignore
    else:
        with open(fr"./{file_name}.{file_type}", mode, encoding=encoding) as f:
            f.write(text)  # type:ignore
    success(f"{file_name}.{file_type} 下载成功")


def download_text_by_response_xpath(
        response,
        xpath,
        split="\n",
        **kwargs
):
    """
    :param response: 网页response
    :param xpath: 网页中需要下载的文本元素xpath
    :param split: 分隔符类型, 默认为换行符
    :return: None


    此函数用于在爬虫任务中，
    通过一个给定的文本元素xpath，快速地进行 文本 下载操作
    """
    text = extract_text_by_response_xpath(response, xpath)  # type: ignore
    download_text(split.join(text), **kwargs)


def download_image_by_response_xpath(
        response,
        xpath,
        **kwargs
):
    """
    :param response: 网页response
    :param xpath: 网页中需要下载的图片元素xpath
    :return: None

    此函数用于在爬虫任务中，
    通过一个给定的图片元素xpath，快速地进行 图片 下载操作
    """
    url_list = extract_link_by_response_xpath(response, xpath)
    for url in url_list:
        download_img(url, **kwargs)


def download_file_by_response_xpath(
        response,
        xpath,
        file_type,
        **kwargs
):
    """
    :param response: 网页response
    :param xpath: 网页中需要下载的附件元素xpath
    :param file_type: 下载文件的后缀名，如果没有指定，则默认为txt
    :return: None

    此函数用于在爬虫任务中，
    通过一个给定的附件元素xpath，快速地进行 附件 下载操作
    """
    url_list = extract_link_by_response_xpath(response, xpath)
    for url in url_list:
        download_file(url, file_type, **kwargs)
