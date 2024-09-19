from log import logger
from tools.request.models import Request, AsyncRequest, SessionRequest, run_script


def test_Request():
    logger.debug(f"{'=' * 20}test_Request start{'=' * 20}")
    req = Request("https://www.baidu.com")

    logger.info(f"req: {req}")
    assert str(req) == "<Request [GET 200 https://www.baidu.com]>"

    logger.info(f"req.url: {req.url}")
    assert req.url == "https://www.baidu.com"

    title = req.xpath("//title/text()").getall()
    logger.info(f"title: {title}")
    assert title == ["百度一下，你就知道"] or title == ["百度一下"]

    logger.info(f"req.text: {req.text[:7]}")
    assert req.text[:7] == "<!DOCTY"

    logger.info(f"req.autodetect_encoding: {req.autodetect_encoding(req.content)}")
    assert req.autodetect_encoding(req.content) == "utf-8"

    logger.info(f"req.urljoin: {req.urljoin('?a=1&b=2')}")
    assert req.urljoin('?a=1&b=2') == "https://www.baidu.com?a=1&b=2"

    logger.info(f"req.status_code: {req.status_code}")
    assert req.status_code == 200

    logger.info(f"req.cookies: {req.cookies}")
    assert req.cookies is not None

    logger.info(f"req.get_cookies_dict: {req.get_cookies_dict()}")
    assert req.cookies is not None
    # assert req.get_cookies_dict() == {
    #     'BAIDUID': 'B4F9B788728D06077380B17813E07FC4:FG=1',
    #     'BAIDUID_BFESS': 'B4F9B788728D06070E054898823DD0DD:FG=1',
    #     'BIDUPSID': 'B4F9B788728D06070E054898823DD0DD',
    #     'PSTM': '1726649240',
    #     'BDSVRTM': '6',
    #     'BD_HOME': '1'
    # }

    logger.debug(f"{'=' * 20}test_Request over{'=' * 20}\n")


async def test_AsyncRequest():
    logger.debug(f"{'=' * 20}test_AsyncRequest start{'=' * 20}")
    async_req = AsyncRequest("http://www.baidu.com", follow_redirects=True)

    await async_req.load_async()

    response = await async_req.set_async_response()

    logger.info(f"async_req: {async_req}")
    assert str(async_req) == "<Request [GET 200 http://www.baidu.com]>"

    logger.info(f"response: {response}")
    assert str(response) == "<Response [200 OK]>"

    logger.info(f"async_req.url: {async_req.url}")
    assert async_req.url == "https://www.baidu.com/" or "https://m.baidu.com/?from=844b&vit=fps"

    title = async_req.xpath("//title/text()").getall()
    logger.info(f"title: {title}")
    assert title == ["百度一下"] or title == ["百度一下，你就知道"]

    logger.info(f"async_req.text: {async_req.text[:7]}")
    assert async_req.text[:7] == "<!DOCTY"

    logger.info(f"async_req.autodetect_encoding: {async_req.autodetect_encoding(async_req.content)}")
    assert async_req.autodetect_encoding(async_req.content) == "utf-8"

    logger.info(f"async_req.urljoin: {async_req.urljoin('?a=1&b=2')}")
    assert async_req.urljoin('?a=1&b=2') == "https://www.baidu.com?a=1&b=2" or "https://m.baidu.com/?a=1&b=2"

    logger.info(f"async_req.status_code: {async_req.status_code}")
    assert async_req.status_code == 200

    logger.info(f"async_req.cookies: {async_req.cookies}")
    assert async_req.cookies is not None

    logger.info(f"async_req.get_cookies_dict: {async_req.get_cookies_dict()}")
    assert async_req.get_cookies_dict() is not None

    logger.debug(f"{'=' * 20}test_AsyncRequest over{'=' * 20}\n")
    # print(async_req.text)


def test_SessionRequest():
    logger.debug(f"{'=' * 20}test_SessionRequest start{'=' * 20}")

    session_req = SessionRequest("https://www.baidu.com")

    logger.info(f"session_req: {session_req}")
    assert str(session_req) == "<Request [GET 200 https://www.baidu.com]>"

    logger.info(f"session_req.url: {session_req.url}")
    assert session_req.url == "https://www.baidu.com"

    title = session_req.xpath("//title/text()").getall()
    logger.info(f"title: {title}")
    assert title == ["百度一下，你就知道"] or title == ["百度一下"]

    logger.info(f"session_req.text: {session_req.text[:7]}")
    assert session_req.text[:7] == "<!DOCTY"

    logger.info(f"session_req.autodetect_encoding: {session_req.autodetect_encoding(session_req.content)}")
    assert session_req.autodetect_encoding(session_req.content) == "utf-8"

    logger.info(f"session_req.urljoin: {session_req.urljoin('?a=1&b=2')}")
    assert session_req.urljoin('?a=1&b=2') == "https://www.baidu.com?a=1&b=2"

    logger.info(f"session_req.status_code: {session_req.status_code}")
    assert session_req.status_code == 200

    logger.info(f"session_req.cookies: {session_req.cookies}")
    assert session_req.cookies is not None

    logger.info(f"session_req.get_cookies_dict: {session_req.get_cookies_dict()}")
    assert session_req.get_cookies_dict() is not None

    logger.debug(f"{'=' * 20}test_SessionRequest over{'=' * 20}\n")


def main2():
    test_SessionRequest()
    test_Request()


if __name__ == '__main__':
    run_script(test_AsyncRequest)
    main2()
