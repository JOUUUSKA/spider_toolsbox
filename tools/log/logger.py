from loguru import logger


def info(msg, *args, **kwargs):
    """
    :param msg: 需要在控制台输出的数据,输出格式为INFO


    此函数用于在控制台输出的数据,输出格式为INFO
    """
    logger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    :param msg: 需要在控制台输出的数据,输出格式为DEBUG


    此函数用于在控制台输出的数据,输出格式为DEBUG
    """
    logger.debug(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """
    :param msg: 需要在控制台输出的数据,输出格式为WARING


    此函数用于在控制台输出的数据,输出格式为WARING
    """
    logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    :param msg: 需要在控制台输出的数据,输出格式为ERROE


    此函数用于在控制台输出的数据,输出格式为ERROE
    """
    logger.error(msg, *args, **kwargs)
