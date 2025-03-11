from spider_toolsbox.tools.constants.constants import (
    image_count,
    txt_count,
    video_count,
    file_count
)
def image_name(value: str = "image_{}"):
    """
    生成名称，多次次生成格式化后的文件名

    :param value: 需格式化的文件名， 默认为image_{}
    :return: 格式化后的文件名
    """
    count = image_count

    def inner():
        nonlocal count
        count += 1
        return value.format(count)

    return inner


def txt_name(value: str = "txt_{}"):
    """
    生成名称，多次次生成格式化后的文件名

    :param value: 需格式化的文件名， 默认为image_{}
    :return: 格式化后的文件名
    """
    count = txt_count

    def inner():
        nonlocal count
        count += 1
        return value.format(count)

    return inner


def video_name(value: str = "video_{}"):
    """
    生成名称，多次次生成格式化后的文件名

    :param value: 需格式化的文件名， 默认为image_{}
    :return: 格式化后的文件名
    """
    count = video_count

    def inner():
        nonlocal count
        count += 1
        return value.format(count)

    return inner

def file_name(value: str = "video_{}"):
    """
    生成名称，多次次生成格式化后的文件名

    :param value: 需格式化的文件名， 默认为image_{}
    :return: 格式化后的文件名
    """
    count = file_count

    def inner():
        nonlocal count
        count += 1
        return value.format(count)

    return inner
