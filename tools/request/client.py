from requests import request
import tools


def get(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送get请求，
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("get", url, headers=headers, params=params, data=data, **kwargs)


def options(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送options请求，
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("options", url, headers=headers, data=data, params=params, **kwargs)


def head(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送head请求
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("head", url, headers=headers, data=data, params=params, **kwargs)


def post(url, headers=None, data=None, json=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送post请求
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("post", url, headers=headers, data=data, json=json, params=params, **kwargs)


def put(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送put请求
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("put", url, headers=headers, data=data, params=params, **kwargs)


def patch(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送patch请求
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("patch", url, headers=headers, data=data, params=params, **kwargs)


def delete(url, headers=None, data=None, params=None, **kwargs):
    """
    :param url: 需要请求的网址
    :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
    :param data: 提交表单，如果没有指定，则默认为None
    :param params: 参数，如果没有指定，则默认为None


    此函数用于模拟requests发送delete请求
    但是有默认的请求头，无需在网页上或第三方库中获取
    """
    if headers is None:
        headers = tools.headers
    return request("delete", url, headers=headers, data=data, params=params, **kwargs)
