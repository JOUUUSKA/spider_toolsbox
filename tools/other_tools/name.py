def image_name(value: str = "image_{}"):
    """
    生成名称，多次次生成格式化后的文件名

    :param value: 需格式化的文件名， 默认为image_{}
    :return: 格式化后的文件名
    """
    count = 0

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
    count = 0

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
    count = 0

    def inner():
        nonlocal count
        count += 1
        return value.format(count)

    return inner
