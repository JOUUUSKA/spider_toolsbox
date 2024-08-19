import re


def html_find_specific_string(text: str, params: str = ""):
    """
    使用re.search，正则解析html文本
    :param text: 正则文本
    :param params: 需要替换的字符串
    :return:

    example：
        raw_text = "onclick="window.open('/njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html');"
        new_text = html_find_specific_string(text, "window.open('{}')")
        print(new_text) => /njweb/zbjh/20240801/9fc5b186-d2ef-4e41-805f-6f4103df9f52.html

    """  # noqa: E501
    pattern = "(.*?)".join([re.escape(s) for s in params.split("{}")])
    values = re.search(pattern, text)
    if values and len(values.groups()) == 1:
        return values.group(1)
    elif values and len(values.groups()) > 1:
        return values.groups()
    else:
        return None
