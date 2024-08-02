import json


def json_loads(data):
    """
    :param data: 需要由 字符串 反序列化为 JSON 的数据
    :return: 由 字符串 反序列化为 JSON 的数据


    此函数用于将 字符串数据 反序列化为 JSON数据
    """
    return json.loads(data)


def json_load(data):
    """
    :param data: 需要由 文件流 反序列化为 JSON 的数据
    :return: 由 文件流 反序列化为 JSON 的数据


    此函数用于将 文件流数据 反序列化为 JSON数据
    """
    return json.load(data)


def json_dump(data, fp):
    """
    :param data: 需要由 JSON 反序列化为 字符串 并 进行持久化储存 的数据
    :param fp: 用fp指代的文件对象       example: with open() as fp:
    :return: 由 JSON 反序列化为 字符串 并 进行持久化储存 的数据


    此函数用于将 JSON数据 反序列化为 字符串数据 并对其进行 持久化储存
    """
    return json.dump(data, fp)


def json_dumps(data):
    """
    :param data: 需要由 JSON 反序列化为 字符串 的数据
    :return: 由 JSON 反序列化为 字符串 的数据


    此函数用于将 JSON数据 反序列化为 字符串数据
    """
    return json.dumps(data)
