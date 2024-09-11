from urllib.parse import urljoin

from requests import request
from scrapy import Selector

import tools
import chardet
from tools.utils.url import is_valid_url


class Request:
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
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.jsondata = jsondata
        self.kwargs = kwargs

        if is_valid_url(url):
            self.url = url
        else:
            raise ValueError(f"Invalid URL: {url}")

        if headers is None:
            self.headers = tools.create_headers()

        self._response = request(
            method.lower(),
            url,
            headers=headers,
            params=params,
            data=data,
            json=jsondata,
            **kwargs
        )
        self.encoding = chardet.detect(self._response.content)['encoding']
        self._response.encoding = str(self.encoding)
        self._tree = Selector(text=self._response.text)

    def __repr__(self):
        return f"<Request [{self.method.upper()} {self.status_code} {self.url}]>"

    def xpath(self, xpath):
        '''
        使用xpath定位元素
        '''
        return self._tree.xpath(xpath)

    @property
    def text(self):
        '''
        返回当前页面的源码
        '''
        return self._response.text

    def urljoin(self, uri):
        '''
        使用urljoin进行url拼接
        '''
        return urljoin(self.url, uri)

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
