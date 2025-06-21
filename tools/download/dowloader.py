import os
import concurrent
from contextlib import _GeneratorContextManager

from tqdm import tqdm
from urllib.parse import urljoin
from typing import Optional, Dict, Any

from tools.constants.constants import EXT_TYPES
from tools.link_extractors.html_response import (
    extract_text_by_response_xpath,
    extract_link_by_response_xpath
)
from concurrent.futures import ThreadPoolExecutor
from tools.log import success, critical, error
from tools.other_tools.name import (
    video_name,
    image_name,
    txt_name,
    file_name as generate_file_name
)
from tools.request import create_default_headers, create_request
from tools.utils.url import is_attachment_href, is_valid_url


class DownloadError(Exception):
    """自定义下载异常"""
    pass


def save_response_content(
        response,
        file_name: str,
        file_type: str,
        file_path: Optional[str] = None,
        mode: str = "wb",
        chunk_size: int = 8192,
        is_streaming_download: bool = False,
        show_progress: bool = True
) -> None:
    # 文件名处理逻辑（保持不变）
    if "." in file_name and file_name.split(".")[-1] in EXT_TYPES:
        if len(file_name.split(".")) >= 2:
            file_name, file_type = os.path.splitext(file_name)
            file_type = file_type.lstrip('.')
        else:
            raise DownloadError(f"Illegal FileName: {file_name}")

    full_name = f"{file_name}.{file_type.lstrip('.')}" if file_type else file_name
    save_path = os.path.join(file_path or ".", full_name) if file_path else full_name

    try:
        if is_streaming_download and isinstance(response, _GeneratorContextManager):
            with response as ctx_response:  # 进入上下文获取真实响应
                ctx_response.raise_for_status()

                # 现在可以访问 headers 了
                total_size = int(ctx_response.headers.get('content-length', 0))
                # todo
                with open(save_path, mode) as file, \
                        tqdm(
                            total=total_size,
                            unit='B',
                            unit_scale=True,
                            desc=f"下载 {full_name}",
                            disable=not show_progress
                        ) as progress_bar:

                    for chunk in ctx_response.iter_bytes(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))

        else:
            if isinstance(response, _GeneratorContextManager) and is_streaming_download == False:
                raise DownloadError("response传入为Stream, 但is_streaming_download=False")
            # 非流式下载处理
            data = response.content
            total_size = len(data)

            with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"下载 {full_name}",
                    disable=not show_progress
            ) as progress_bar:
                with open(save_path, mode) as file:
                    file.write(data)
                    progress_bar.update(total_size)

        success(f"文件保存成功: {save_path}")
    except Exception as e:
        critical(f"文件保存失败: {save_path} - {str(e)}")
        raise DownloadError(f"文件保存错误: {str(e)}") from e


def download_video(
        url: str,
        method: str = "get",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        file_name: Optional[str] = None,
        file_type: str = "mp4",
        file_path: Optional[str] = None,
        mode: str = "wb",
        is_streaming_download: bool = False,
        **kwargs
) -> None:
    """
    下载视频文件

    Args:
        url: 视频资源URL
        method: HTTP方法 (默认: get)
        headers: 请求头 (默认: 自动生成)
        data: 请求体数据
        params: 请求参数
        file_name: 文件名 (默认: 自动生成)
        file_type: 文件扩展名 (默认: mp4)
        file_path: 存储目录 (可选)
        mode: 文件写入模式 (默认: wb)
        is_streaming_download: 是否开启流式下载 (默认: False)
        **kwargs: 其他请求参数

    Raises:
        DownloadError: 下载过程中出现错误
    """
    try:
        # 设置默认值
        headers = headers or create_default_headers()
        file_name = file_name or video_name()

        # 发送请求并保存
        response = create_request(
            url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            **kwargs
        )
        save_response_content(
            response=response,
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
            is_streaming_download=is_streaming_download,
            mode=mode
        )
    except Exception as e:
        critical(f"视频下载失败: {url} - {str(e)}")
        raise DownloadError(f"视频下载错误: {str(e)}") from e


def download_m3u8(
        m3u8_url: str,
        output_name: str = "output",
        file_path: Optional[str] = None,
        max_workers: int = 8,
        chunk_size: int = 8192,
        is_streaming_download: bool = False,
        show_progress: bool = True,
        **kwargs
) -> str:
    """
    M3U8流媒体下载器

    Args:
        m3u8_url: m3u8索引文件地址
        output_name: 输出文件名（不含后缀）
        file_path: 存储路径（可选）
        max_workers: 最大并发线程数（默认: 8）
        is_streaming_download: 是否开启流式下载 (默认: False)
        chunk_size: 流式下载中每次读取的内容大小 (默认: 8192)
        show_progress: 是否开启进度可视化 (默认: True)
        **kwargs: 其他请求参数

    Returns:
        str: 合并后的文件路径

    Raises:
        DownloadError: 下载过程中出现错误
    """
    try:
        # 创建临时目录
        base_path = file_path or os.getcwd()
        temp_dir = os.path.join(base_path, "ts_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # 获取M3U8内容
        response = create_request(m3u8_url, **kwargs)
        if response.status_code != 200:
            raise DownloadError(f"获取M3U8失败: {response.status_code}")

        # 解析TS片段列表
        ts_list = [
            urljoin(m3u8_url, line.strip())
            for line in response.text.splitlines()
            if line.strip() and not line.startswith("#")
        ]

        # 下载TS片段
        def _download_segment(ts_url: str, index: int) -> str:
            """下载单个TS片段"""
            segment_path = os.path.join(temp_dir, f"seg_{index:04d}.ts")
            try:
                if is_streaming_download:
                    with create_request(ts_url, stream=True, **kwargs) as ctx_response:
                        ctx_response.raise_for_status()
                        total_size = int(ctx_response.headers.get('content-length', 0))
                        with open(segment_path, "wb") as file, \
                                tqdm(
                                    total=total_size,
                                    unit='B',
                                    unit_scale=True,
                                    desc=f"下载 {ts_url}",
                                    disable=not show_progress
                                ) as progress_bar:
                            for chunk in ctx_response.iter_bytes(chunk_size=chunk_size):
                                if chunk:
                                    file.write(chunk)
                                    progress_bar.update(len(chunk))
                else:
                    # 非流式下载处理
                    data = create_request(ts_url, **kwargs).content
                    total_size = len(data)

                    with tqdm(
                            total=total_size,
                            unit='B',
                            unit_scale=True,
                            desc=f"下载 {ts_url}",
                            disable=not show_progress
                    ) as progress_bar:
                        with open(segment_path, "wb") as file:
                            file.write(data)
                            progress_bar.update(total_size)

                return segment_path
            except Exception as e:
                error(f"片段下载失败: {ts_url} - {str(e)}")
                raise DownloadError(f"TS片段下载错误: {str(e)}") from e

        # 使用线程池并发下载
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_download_segment, url, idx): (url, idx)
                for idx, url in enumerate(ts_list)
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    critical("M3U8下载任务失败")
                    raise DownloadError("TS片段下载失败") from e

        # 合并TS文件
        output_path = os.path.join(base_path, f"{output_name}.mp4")
        with open(output_path, "wb") as output_file:
            for idx in range(len(ts_list)):
                segment_path = os.path.join(temp_dir, f"seg_{idx:04d}.ts")
                try:
                    with open(segment_path, "rb") as segment_file:
                        output_file.write(segment_file.read())
                    os.remove(segment_path)
                except FileNotFoundError:
                    critical(f"片段文件不存在: {segment_path}")
                    continue

        # 清理临时目录
        os.rmdir(temp_dir)
        success(f"M3U8合并完成: {output_path}")
        return output_path

    except Exception as e:
        critical(f"M3U8处理失败: {m3u8_url} - {str(e)}")
        raise DownloadError(f"M3U8处理错误: {str(e)}") from e


def download_file(
        file_url: str,
        file_type: str,
        file_name: Optional[str] = None,
        method: str = "get",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        mode: str = "wb",
        file_path: Optional[str] = None,
        is_streaming_download: bool = False,
        **kwargs
) -> None:
    """
    下载通用文件

    Args:
        file_url: 文件URL
        file_type: 文件扩展名
        file_name: 文件名 (默认: 自动生成)
        method: HTTP方法 (默认: get)
        headers: 请求头 (默认: 自动生成)
        data: 请求体数据
        params: 请求参数
        mode: 文件写入模式 (默认: wb)
        file_path: 存储目录 (可选)
        is_streaming_download: 是否开启流式下载 (默认: False)
        **kwargs: 其他请求参数

    Raises:
        ValueError: URL无效时
        DownloadError: 下载过程中出现错误
    """
    try:
        # 验证URL
        if not (is_attachment_href(file_url) or is_valid_url(file_url)):
            raise ValueError(f"无效文件URL: {file_url}")

        # 设置默认值
        headers = headers or create_default_headers()
        file_name = file_name or generate_file_name()

        # 发送请求并保存
        response = create_request(
            file_url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            **kwargs
        )
        save_response_content(
            response=response,
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
            is_streaming_download=is_streaming_download,
            mode=mode
        )
    except Exception as e:
        critical(f"文件下载失败: {file_url} - {str(e)}")
        raise DownloadError(f"文件下载错误: {str(e)}") from e


def download_image(
        url: str,
        method: str = "get",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        file_name: Optional[str] = None,
        file_type: str = "jpg",
        mode: str = "wb",
        file_path: Optional[str] = None,
        is_streaming_download: bool = False,
        **kwargs
) -> None:
    """
    下载图片文件

    Args:
        url: 图片资源URL
        method: HTTP方法 (默认: get)
        headers: 请求头 (默认: 自动生成)
        data: 请求体数据
        params: 请求参数
        file_name: 文件名 (默认: 自动生成)
        file_type: 文件扩展名 (默认: jpg)
        mode: 文件写入模式 (默认: wb)
        file_path: 存储目录 (可选)
        is_streaming_download: 是否开启流式下载 (默认: False)
        **kwargs: 其他请求参数

    Raises:
        DownloadError: 下载过程中出现错误
    """
    try:
        # 设置默认值
        headers = headers or create_default_headers()
        file_name = file_name or image_name()

        # 发送请求并保存
        response = create_request(
            url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            **kwargs
        )
        save_response_content(
            response=response,
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
            is_streaming_download=is_streaming_download,
            mode=mode
        )
    except Exception as e:
        critical(f"图片下载失败: {url} - {str(e)}")
        raise DownloadError(f"图片下载错误: {str(e)}") from e


def download_text(
        content: str,
        file_name: Optional[str] = None,
        file_type: str = "txt",
        mode: str = "w",
        file_path: Optional[str] = None,
        encoding: str = "utf-8",
        **kwargs
) -> None:
    """
    保存文本内容到文件

    Args:
        content: 文本内容
        file_name: 文件名 (默认: 自动生成)
        file_type: 文件扩展名 (默认: txt)
        mode: 文件写入模式 (默认: w)
        file_path: 存储目录 (可选)
        encoding: 文件编码 (默认: utf-8)
    """
    # 设置默认值
    file_name = file_name or txt_name()

    # 构建安全文件路径
    full_name = f"{file_name}.{file_type.lstrip('.')}"
    save_path = os.path.join(file_path or ".", full_name) if file_path else full_name
    try:
        # 写入文件
        with open(save_path, mode, encoding=encoding) as file:
            file.write(content)
        success(f"文本保存成功: {save_path}")
    except OSError as e:
        critical(f"文本保存失败: {save_path} - {str(e)}")
        raise DownloadError(f"文本保存错误: {str(e)}") from e


def download_text_by_response_xpath(
        response,
        xpath: str,
        separator: str = "\n",
        **kwargs
) -> None:
    """
    通过XPath提取文本并保存

    Args:
        response: 网页响应对象
        xpath: 文本元素的XPath表达式
        separator: 文本分隔符 (默认: 换行符)
        **kwargs: 传递给download_text的额外参数
    """
    try:
        extracted_text = extract_text_by_response_xpath(response, xpath)
        if not extracted_text:
            raise DownloadError("未提取到文本内容")

        download_text(
            content=separator.join(extracted_text),
            **kwargs
        )
    except Exception as e:
        critical(f"XPath文本提取失败: {response.url} {xpath} - {str(e)}")


def download_image_by_response_xpath(
        response,
        xpath: str,
        is_streaming_download: bool = False,
        **kwargs
) -> None:
    """
    通过XPath提取图片并下载

    Args:
        response: 网页响应对象
        xpath: 图片元素的XPath表达式
        is_streaming_download: 是否开启流式下载 (默认: False)
        **kwargs: 传递给download_image的额外参数
    """
    try:
        image_urls = extract_link_by_response_xpath(response, xpath)
        if not image_urls:
            error("未提取到图片URL")
            return

        for url in image_urls:
            try:
                download_image(url, is_streaming_download=is_streaming_download, **kwargs)
            except DownloadError:
                error(f"图片下载跳过: {url}")
                continue
    except Exception as e:
        critical(f"XPath图片提取失败: {xpath} - {str(e)}")
        raise DownloadError(f"图片提取错误: {str(e)}") from e


def download_file_by_response_xpath(
        response,
        xpath: str,
        file_type: str,
        is_streaming_download: bool = False,
        **kwargs
) -> None:
    """
    通过XPath提取文件并下载

    Args:
        response: 网页响应对象
        xpath: 文件元素的XPath表达式
        file_type: 文件扩展名
        **kwargs: 传递给download_file的额外参数
    """
    try:
        file_urls = extract_link_by_response_xpath(response, xpath)
        if not file_urls:
            error("未提取到文件URL")
            return

        for url in file_urls:
            try:
                download_file(url, file_type=file_type, is_streaming_download=is_streaming_download, **kwargs)
            except DownloadError:
                error(f"文件下载跳过: {url}")
                continue
    except Exception as e:
        critical(f"XPath文件提取失败: {xpath} - {str(e)}")
        raise DownloadError(f"文件提取错误: {str(e)}") from e
