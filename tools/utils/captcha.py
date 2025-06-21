from httpx import Response as HttpxResponse
from loguru import logger
from typing import Any, Dict, Optional

from tools.download import DownloadError
from tools.ocr import recognize_text_captcha
from tools.request import create_request


def request_with_captcha(
        target_url: str,
        captcha_url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        target_params: Optional[Dict[str, str]] = None,
        target_data: Dict[str, Any] = None,
        target_json: Optional[Dict[str, str]] = None,
        captcha_params: Optional[Dict[str, str]] = None,
        captcha_data: Optional[Dict[str, str]] = None,
        captcha_json: Optional[Dict[str, str]] = None,
        captcha_processor: callable = recognize_text_captcha,
        captcha_field: str = "captcha",
        captcha_position: str = "body",  # 'body', 'params', 'query'
        target_method: str = "POST",
        captcha_method: str = "GET",
        **kwargs
) -> HttpxResponse:
    """
    带验证码的通用请求函数

    Args:
        target_url: 目标请求的URL
        captcha_url: 验证码图片的URL
        headers: 额外的请求头
        target_params: 额外的params请求参数
        target_data: 目标表单数据
        target_json: 额外的json请求参数
        captcha_params: 验证码的params请求参数
        captcha_data: 验证码的表单请求参数
        captcha_json: 验证码的json请求参数
        captcha_field: 验证码在请求中的字段名
        captcha_position: 验证码存放位置 ('body', 'params', 'query')
        captcha_processor: 验证码处理函数
        target_method: 目标url请求方法 (POST/GET)
        captcha_method: 验证码请求方法 (GET/POST)
        request_kwargs: 传递给create_request的其他参数

    Returns:
        HttpxResponse: 登录请求的响应对象

    Examples:
        1、captcha字段在data里面时:
        ```
            target_url = "https://xxx.com/authserver/login
            captcha_url = "https://xxx.com/authserver/getCaptcha.htl"

            data = {
                'username': '123456',
                'password': '123456',
                'captcha': 'captcha',
            }

            response = request_with_captcha(
                target_url,
                captcha_url,
                target_data=data,
                target_method="get",
                captcha_method='get',
                captcha_field="captcha",
                captcha_position="body",
            )
        ```



        2、captcha字段在params里面时:
        ```
            target_url = "https://xxx.com/authserver/login
            captcha_url = "https://xxx.com/authserver/getCaptcha.htl"

            params = {
            'timestamp': '1782394712921',
            'captcha': 'captcha',
            }


            response = request_with_captcha(
                target_url,
                captcha_url,
                target_params=params,
                target_method="get",
                captcha_method='get',
                captcha_field="captcha",
                captcha_position="params",
            )
        ```

        3、captcha字段在url里面时:
        ```
            target_url = "https://xxx.com/authserver/download.jsp?urltype=news.DownloadAttachUrl
            captcha_url = "https://xxx.com/authserver/getCaptcha.htl"

            response = request_with_captcha(
                target_url,
                captcha_url,
                target_method="get",
                captcha_method='get',
                captcha_field="captcha",
                captcha_position="query",
            )
        ```
    """
    try:
        # 1. 获取验证码
        captcha_kwargs = {
            "method": captcha_method,
            "headers": headers,
            "params": captcha_params,
            "data": captcha_data,
            "jsondata": captcha_json,
            **kwargs.get("captcha_kwargs", {}),
        }
        if captcha_kwargs.get("stream") is not None and captcha_kwargs.get("stream") == True:
            del captcha_kwargs["stream"]

        captcha_response = create_request(captcha_url, **captcha_kwargs)
        captcha_response.raise_for_status()

        # 2. 处理验证码
        captcha_cookies = captcha_response.get_cookies_dict()
        captcha_result = captcha_processor(captcha_response.content)

        # 3. 准备登录请求
        # 根据位置添加验证码到请求数据
        # target_data = target_data.copy()
        if captcha_position == "body":
            target_data[captcha_field] = captcha_result
        elif captcha_position == "params":
            target_params = target_params.copy() if target_params else {}
            target_params[captcha_field] = captcha_result
        elif captcha_position == "query":
            # 直接添加到URL查询参数
            from urllib.parse import urlencode
            separator = "&" if "?" in target_url else "?"
            target_url = f"{target_url}{separator}{captcha_field}={captcha_result}"

        # 4. 发送目标url请求
        target_kwargs = {
            "method": target_method,
            "data": target_data,
            "headers": headers,
            "params": target_params,
            "cookies": captcha_cookies,
            "jsondata": target_json,
            **kwargs.get("target_kwargs", {})
        }
        target_response = create_request(target_url, **target_kwargs)
        logger.success("验证码打码成功")
        if (not kwargs) or (kwargs.get("target_kwargs").get("stream") is not None and kwargs.get("target_kwargs").get("stream") == False):
            target_response.raise_for_status()
            return target_response
        elif (kwargs) and (kwargs.get("target_kwargs") is not None and kwargs.get("target_kwargs").get("stream") is not None and kwargs.get("target_kwargs").get("stream") == True):
            return target_response._response
        else:
            target_response.raise_for_status()
            return target_response



    except Exception as e:
        raise DownloadError(f"验证码打码过程中出错: {str(e)}")
        # 返回包含错误信息的响应对象
        # return HttpxResponse(
        #     status_code=500,
        #     request=target_response.request if 'target_response' in locals() else None,
        #     content=f"captcha request failed: {str(e)}".encode()
        # )
