from lxml import etree


def xpath(self, res, x_path):
    """
    :param res: 原始HTML字符串
    :param x_path: 根据传入的原始HTML字符串，使用XPATH进行元素定位
    :return: 使用XPATH定位到的网页元素


    此函数用于通过对传入的原始HTML字符串，
    使用XPATH进行元素定位，
    并且返回定位到的元素
    """
    tree = etree.HTML(res)
    return tree.xpath(x_path)
