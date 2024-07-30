import execjs


def open_js(js: str, path: bool = True):
    """
    打开JS文件，
    返回一个编译后，可直接调用的JS环境

    :param js: js文件
    :param path: 是否为地址, 默认True
    :return: JS环境
    """
    if path:
        ctx = execjs.compile(open(js, "r", encoding="utf8").read())
    else:
        ctx = execjs.compile(js)
    return ctx


def generate_name(value: str):
    """
    生成名称，根据调用次数生成

    :param value: _description_
    """
    pass
