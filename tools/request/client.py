from spider_toolsbox.tools.request.models import Request, SessionRequest, AsyncRequest

classes_dict = {
    "Request": Request,
    "SessionRequest": SessionRequest,
    "AsyncRequest": AsyncRequest,
}


def create_request(url, req_mode="Request", *args, **kwargs):
    '''
    基于工厂模式的生产函数，用于创建初始化不同的请求类型
    类型有三: 同步、异步、会话
    分别用形参的
    req_mode="Request",
    req_mode="SessionRequest",
    req_mode="AsyncRequest"
    进行区分并初始化，默认为"Request"

    特殊的,
    使用req_mode="AsyncRequest"初始化异步函数时，
    在初始化后需要手动执行load_async方法，
    load_async方法是一个异步函数，所以同时用await挂起。

    example:
        req_mode3 = "AsyncRequest"
        urequest3 = [create_request(url=url, req_mode=req_mode3, headers=headers) for url in urls]
        await asyncio.gather(*[req.load_async() for req in requests])
        for req in urequest3:
            title = req.xpath("xpath").get()
            assert req.xpath("//title/text()").get() == "百度一下，你就知道"
    '''

    classes = classes_dict.get(req_mode)
    if classes:
        return classes(url, *args, **kwargs)
    else:
        raise ValueError(
            f"Only support request modes: {', '.join(classes_dict.keys())}, "
            f"But got: {req_mode}"
        )
