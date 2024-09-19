from urllib.parse import urljoin

import chardet
from scrapy import Selector

import tools
from tools.utils.url import is_valid_url
from utils.xpath import is_valid_xpath


class BaseClient(object):
    '''
    请求类的基类，定义了几个接口函数
    '''
    def set_response(self):
        raise NotImplementedError

    async def set_async_response(self):
        raise NotImplementedError

    def text(self):
        raise NotImplementedError

    def url(self):
        raise NotImplementedError

    def urljoin(self, uri):
        raise NotImplementedError

    def json(self):
        raise NotImplementedError

    def status_code(self):
        raise NotImplementedError

    def cookies(self):
        raise NotImplementedError

    def get_cookies_dict(self):
        raise NotImplementedError

    def content(self):
        raise NotImplementedError

    def xpath(self, xpath):
        raise NotImplementedError


class BaseRequest(BaseClient):
    '''
    继承于基类，并且实现了基类里面的接口函数
    '''
    def __init__(
            self,
            url,
            method="get",
            headers=None,
            params=None,
            data=None,
            jsondata=None,
            **kwargs
    ):
        '''
        同步初始化
        '''
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.jsondata = jsondata

        if is_valid_url(url):
            self.req_url = url
        else:
            raise ValueError(f"Invalid URL: {url}")

        if headers is None:
            self.headers = tools.create_default_headers()

        self._response = self.set_response(**kwargs)

        self._response.default_encoding = self.autodetect_encoding(self._response.content)

    async def __ainit__(
            self,
            url,
            method="get",
            headers=None,
            params=None,
            data=None,
            jsondata=None,
            **kwargs
    ):
        '''
        异步初始化，需要手动执行load_async方法并await挂起
        '''
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.jsondata = jsondata

        if is_valid_url(url):
            self.req_url = url
        else:
            raise ValueError(f"Invalid URL: {url}")

        if headers is None:
            self.headers = tools.create_headers()

        self._response = await self.set_async_response(**kwargs)

        self._response.default_encoding = self.autodetect_encoding(self._response.content)

    def __repr__(self):
        '''
        定义Request的样式
        '''
        return f"<Request [{self.method.upper()} {self.status_code} {self.req_url}]>"

    def set_response(self, **kwargs):
        '''
        父类制定的同步接口方法，需要子类实现
        '''
        raise NotImplementedError("response must be set")

    async def set_async_response(self, **kwargs):
        '''
        父类制定的异步接口方法，需要子类实现
        '''
        raise NotImplementedError("async_response must be set")

    def autodetect_encoding(self, content):
        '''
        传入response.content，自动获取编码格式，防止乱码
        '''
        encoding = chardet.detect(content).get('encoding', "utf-8")
        return str(encoding)

    def xpath(self, xpath):
        '''
        使用xpath定位元素
        '''
        selector = Selector(text=self._response.text)
        if not selector:
            raise RuntimeError("No response received yet")
        if not is_valid_xpath(xpath):
            raise ValueError(f"Invalid XPath: {xpath}")
        return selector.xpath(xpath)

    @property
    def text(self):
        '''
        返回当前页面的源码
        '''
        return self._response.text

    @property
    def url(self):
        '''
        返回当前界面的url
        '''
        return self._response.url

    def urljoin(self, uri):
        '''
        使用urljoin进行url拼接
        '''

        return urljoin(str(self.url), uri)

    def json(self):
        '''
        返回json格式的响应数据
        '''
        return self._response.json()

    @property
    def status_code(self):
        '''
        返回网页响应码
        '''
        return self._response.status_code

    @property
    def content(self):
        '''
        返回响应字节流
        '''
        return self._response.content

    @property
    def cookies(self):
        '''
        返回当前页面设置的cookies
        '''
        return self._response.cookies

    def get_cookies_dict(self):
        '''
        返回当前页面设置的cookies_dict
        '''
        cookies_dict = {k: v for k, v in self.cookies.items()}
        return cookies_dict
