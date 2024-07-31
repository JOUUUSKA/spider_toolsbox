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


def rebuidtext(self, res: str):
    """
    :param res: 原始HTML字符串
    :return: 重构后的HTML字符串

    此函数用于重构response响应

    常见的打印页面报错如下:
    UnicodeEncodeError: ‘gbk’ codec can’t encode character ‘\xe7’ in position 318: illegal multibyte sequence
    中文翻译为UnicodeEncodeError：‘gbk’编解码器无法在位置318中编码字符’\ xe7’：非法的多字节序列

    很多时候页面返回的response响应无法进行打印输出，
    最常用的方法就是对response进行重构，
    完成后即可打印输出

    值得一提，此方法并不是通解，
    如果调用此函数对response进行重构后，仍然不能打印页面，请另寻办法解决。

    笔者在此列出两条本人常用的解决办法，可供各位参考:
    1、调用此方法对response进行重构;
    2、在Python文件最上方加入如下代码:
        import sys,io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
        #'gb18030'可修改为ISO-8859-1,gb2312。依据具体情况自行更换即可
    """
    return res.encode("ISO-8859-1").decode("utf8")
