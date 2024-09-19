from tools import create_default_headers
from tools.request.client import create_request
from tools.request.models import run_script

url = "https://www.baidu.com"
headers = create_default_headers()

def test_Request_create_request():
    req_mode1 = "Request"
    urequest1 = create_request(url=url, req_mode=req_mode1, headers=headers)
    assert urequest1.xpath("//title/text()").get() == "百度一下，你就知道"


def test_Session_Request_create_request():
    req_mode2 = "SessionRequest"
    urequest2 = create_request(url=url, req_mode=req_mode2, headers=headers)
    assert urequest2.xpath("//title/text()").get() == "百度一下，你就知道"



async def test_Async_Request_create_request():
    req_mode3 = "AsyncRequest"
    urequest3 = create_request(url=url, req_mode=req_mode3, headers=headers)
    await urequest3.load_async()
    assert urequest3.xpath("//title/text()").get() == "百度一下，你就知道"


async def main():
    test_Request_create_request()
    test_Session_Request_create_request()
    await test_Async_Request_create_request()

if __name__ == '__main__':
    run_script(main)

