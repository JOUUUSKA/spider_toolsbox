import re


def regex(self, res, str_1, str_2):
    """
    :param res: 原始内容 或 原始响应
    :param str_1: 第一部分的分割范围
    :param str_2: 第二部分的分割范围
    :return: 分割范围之间的所有字符串


    此函数用于返回一个列表，
    列表中的元素为 第一个 符合给定范围条件 之间的字符串

    使用实例:
    a = 123aaa456bbb456ccc456
    print(spider_tools().re(a,'123','456')) ==> aaa
    """

    pattern = re.compile(r"{}(.*?){}".format(re.escape(str_1), re.escape(str_2)))
    values = re.findall(pattern, res)
    return values
