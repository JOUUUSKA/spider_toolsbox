import asyncio

import httpx

from request.base_client import BaseRequest


class Request(BaseRequest):
    '''
    同步请求的Request
    '''
    def set_response(self, **kwargs):
        self._response = httpx.request(
            self.method.lower(),
            self.req_url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            json=self.jsondata,
            **kwargs
        )
        return self._response


class SessionRequest(BaseRequest):
    '''
    会话请求的Request
    '''
    def set_response(self, **kwargs):
        self._response = httpx.Client().request(
            self.method.upper(),
            self.req_url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            json=self.jsondata,
            **kwargs
        )
        return self._response


class AsyncRequest(BaseRequest):
    '''
    异步请求的Request
    '''
    def __init__(
            self,
            url,
            method="get",
            headers=None,
            params=None,
            data=None,
            jsondata=None,
            follow_redirects=False,
            **kwargs
    ):
        self.follow_redirects = follow_redirects
        self._ainit_coroutine = self.__ainit__(
            url,
            method=method,
            headers=headers,
            params=params,
            data=data,
            jsondata=jsondata,
            **kwargs
        )

    async def set_async_response(self, **kwargs):
        async with httpx.AsyncClient(follow_redirects=self.follow_redirects) as client:
            self._response = await client.request(
                self.method.upper(),
                self.req_url,
                headers=self.headers,
                params=self.params,
                data=self.data,
                json=self.jsondata,
                **kwargs
            )
        return self._response

    async def load_async(self):
        '''
        异步函数初始化必须手动执行的初始化操作
        '''
        await self._ainit_coroutine


def run_script(func, *args, **kwargs):
    '''
    用于在主函数中，执行异步任务
    '''
    asyncio.run(func(*args, **kwargs))
