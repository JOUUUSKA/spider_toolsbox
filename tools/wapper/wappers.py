import time


def catch_bug(func):
    """
    :param func: 需要传入的函数
    :return: 传入的原函数


    此函数用于快速将函数加入到 try-except 语句，防止报错影响下游函数的处理，
    在报错时，会在控制台显示抛出错误的函数名称，用于快速定位

    使用示例:
        @spidertool.catch_bug
        def test_func():
            raise Exception('测试函数报错了')

        if __name__ == '__main__':
            test_func() ==> test_func 抛出异常，异常已捕获，内容如下:测试函数报错了
    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"{func.__name__} 抛出异常，异常已捕获，内容如下:\n {e}")

    return wrapper


def test_time(func):
    """
    :param func: 需要传入的函数
    :return: 传入的原函数所耗费的时间


    此函数用于测试函数运行时间

    使用示例:
        @spidertool.test_time
        def test_func():sleep(2)

        if __name__ == '__main__':
            test_func ==> test_func 函数在 0m 2s 内完成
    """

    def target(*args, **kwargs):
        since = time.time()
        result = func()
        time_elapsed = time.time() - since
        print(func.__name__, "函数在 {:.0f}m {:.0f}s 内完成".format(time_elapsed // 60, time_elapsed % 60))
        return result

    return target()


def retry(max_attempts: int, delay):
    """
    :param max_attempts: 需要重试的最大次数
    :param delay: 每次重试的时间间隔
    :return: 传入的原函数


    此函数用于将可能发生错误的函数进行重试，
    程序抛出的错误将在最后一次重试失败后打印输出到控制台

    重试次数 与 重试间隔 自行指定

    使用示例:
    @spidertool.retry(max_attempts=5, delay=2) 或 @spidertool.retry(5, 2)
    def test_func():
        raise Exception('报错了')

    if __name__ == '__main__':
        test_func() ==> 捕获到aaa异常，将在 2 秒后进行第 1 次重试
                        捕获到aaa异常，将在 2 秒后进行第 2 次重试
                        捕获到aaa异常，将在 2 秒后进行第 3 次重试
                        捕获到aaa异常，将在 2 秒后进行第 4 次重试
                        捕获到aaa异常，将在 2 秒后进行第 5 次重试
                        aaa异常情况如下:报错了

                        Traceback (most recent call last):
                            File "D:\pythonProject\草稿.py", line 18, in <module>
                            test_func()
                            File "D:\pythonProject\Spider_ToolBox\SpiderTools.py", line 667, in wrapper
                            raise Exception("已达到所设置的{}次最大重试次数".format(max_attempts))
                        Exception: 已达到所设置的5次最大重试次数

                        进程已结束,退出代码1
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            exception = None
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"捕获到{func.__name__}异常，将在 {delay} 秒后进行第 {attempts + 1} 次重试")
                    attempts += 1
                    time.sleep(delay)
                    exception = e
            print(f"{func.__name__}异常情况如下\n{exception}")
            raise Exception("已达到所设置的{}次最大重试次数".format(max_attempts))

        return wrapper

    return decorator
