import pytest

from tools.request.client import Request


class TestRequest:
    def __init__(self):
        self.req = Request('https://www.baidu.com/', method='get')

    def test_repr(self):
        assert self.req.__repr__() == f"<Request [GET 200 https://www.baidu.com/]>"

    def test_xpath(self):
        assert self.req.xpath("//*[@id='su']/@value") == "百度一下"

    def test_text(self):
        url = "https://ztbgl.yangtzeu.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid=14130&owner=1959294575&clicktype=wbnews"
        req = Request(url, method="post")
        assert req.text == "307"

    def test_urljoin(self):
        uri = "?a=1&b=2"
        assert self.req.urljoin(uri) == "https://www.baidu.com/?a=1&b=2"

    def test_status_code(self):
        assert self.req.status_code == 200
