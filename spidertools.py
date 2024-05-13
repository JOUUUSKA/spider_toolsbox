# -*- coding: UTF-8 -*-
'''
@Project ：crawl
@File    ：spider_tools.py
@IDE     ：PyCharm
@Author  ：JOUSKA.
@Date    ：2023/12/14 10:50
'''
import base64
import hashlib
import hmac
import json
import os
import random
import re
import time

import cv2
import ddddocr
import execjs
import jwt
import requests
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from fake_useragent import UserAgent
from loguru import logger
from lxml import etree


class SpiderTools:
    def __init__(self):
        '''
        进行请求头初始化设置
        '''
        self.headers = {'User-Agent': UserAgent().random}
        self.image_count = 0
        self.txt_count = 0
        self.video_count = 0

    def open_js(self, js):
        '''
        :param js: 需要打开的JS文件路径
        :return: 返回给编译好,可调用的JS环境


        此函数用于方便使用者快速打开一个JS文件，
        并且返回一个 基于此JS文件 编译好的，可直接调用的JS环境
        '''
        ctx = execjs.compile(open(js, 'r', encoding='utf8').read())
        return ctx

    def image_name(self):
        '''
        :return: 根据调用次数，返回一个有序的文件名


        此函数用于和 download_image函数 进行合作，
        在下载图片时，对图片文件进行有序化命名,
        有序化命名的示例: image_1,image_2,image_3
        '''
        self.image_count += 1
        return f"image_{self.image_count}"

    def txt_name(self):
        '''
        :return: 调用时根据调用次数，返回一个有序的文件名


        此函数用于和 download_character函数 进行合作，
        在下载文本时，对文本文件进行有序化命名,
        有序化命名的示例: txt_1,txt_2,txt_3
        '''
        self.txt_count += 1
        return f"image_{self.txt_count}"

    def video_name(self):
        '''
        :return: 调用时根据调用次数，返回一个有序的文件名


        此函数用于和 download_video函数 进行合作，
        在下载视频时，对视频文件进行有序化命名,
        有序化命名的示例: video_1,video_2,video_3
        '''
        self.video_count += 1
        return f"image_{self.video_count}"

    def download_video(self, url, headers=None, data=None, params=None, name=None, type_=None, mode=None, **kwargs):
        '''
        :param url: 需要下载的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None
        :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
        :param type_: 下载文件的后缀名，如果没有指定，则默认为mp4
        :param mode: 下载文件时的模式，如果没有指定，则默认为wb
        :return:None


        此函数用于在爬虫任务中，
        通过一个给定的URL，快速地进行 视频 下载操作

        URL为必填，其他参数为选填，
        如果:
        对其他参数没有进行特别指定，
        那么:
        headers 默认为 self.headers
        type_ 默认为 'mp4'
        name 默认为 str(self.video_name()
        mode 默认为 'wb'

        并在此文件夹下新建一个Download_video文件夹，对下载的视频进行持久化存储
        '''
        if type_ is None:
            type_ = 'mp4'
        if name is None:
            name = str(self.video_name())
        if mode is None:
            mode = 'wb'
        if headers is None:
            headers = self.headers
        if not os.path.exists('./Download_video'):
            os.mkdir('./Download_video')
        response = requests.get(url, headers=headers, data=data, params=params, **kwargs)
        if response.status_code == 200:
            with  open(f"./Download_video/{name}.{type_}", mode) as f:
                f.write(response.content)
                print(f"{name}.{type_} 下载成功")
        else:
            print(f"{name}.{type_} 下载失败")

    def download_img(self, url, headers=None, data=None, params=None, name=None, type_=None, mode=None, **kwargs):
        '''
        :param url: 需要下载的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None
        :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
        :param type_: 下载文件的后缀名，如果没有指定，则默认为jpg
        :param mode: 下载文件时的模式，如果没有指定，则默认为wb
        :return:None


        此函数用于在爬虫任务中，
        通过一个给定的URL，快速地进行 图片 下载操作

        URL为必填，其他参数为选填，
        如果:
        对其他参数没有进行特别指定，
        那么:
        headers 默认为 self.headers
        type_ 默认为 'jpg'
        name 默认为 str(self.image_name()
        mode 默认为 'wb'

        并在此文件夹下新建一个Download_image文件夹，对下载的 图片 进行持久化存储
        '''
        if type_ is None:
            type_ = 'jpg'
        if name is None:
            name = str(self.image_name())
        if mode is None:
            mode = 'wb'
        if headers is None:
            headers = self.headers
        if not os.path.exists('./Download_img'):
            os.mkdir('./Download_img')
        response = requests.get(url, headers=headers, data=data, params=params, **kwargs)
        if response.status_code == 200:
            with  open(f"./Download_img/{name}.{type_}", mode) as f:
                f.write(response.content)
                print(f"{name}.{type_} 下载成功")
        else:
            print(f"{name}.{type_} 下载失败")

    def download_character(self, txt, name=None, type_=None, mode=None):
        '''
        :param txt: 需要下载的 文字 或 响应
        :param name: 下载时文件的命名，如果没有指定，则默认为字符串形式的时间戳
        :param type_: 下载文件的后缀名，如果没有指定，则默认为txt
        :param mode: 下载文件时的模式，如果没有指定，则默认为w
        :return: None


        此函数用于在爬虫任务中，
        通过一个给定的文本，快速地进行 文本 下载操作

        TXT为必填，其他参数为选填，
        如果:
        对其他参数没有进行特别指定，
        那么:
        type_ 默认为 'txt'
        name 默认为 str(self.txt_name()
        mode 默认为 'w'

        并在此文件夹下新建一个Download_txt文件夹，对下载的 文本 进行持久化存储
        '''
        if type_ is None:
            type_ = 'txt'
        if name is None:
            name = str(self.txt_name())
        if mode is None:
            mode = 'w'
        if not os.path.exists('./Download_txt'):
            os.mkdir('./Download_txt')
        with  open(f"./Download_txt/{name}.{type_}", mode) as f:
            f.write(txt)

    def ocr_img(self, img_path):
        '''
        :param imgpath: 需要识别的图片路径
        :return: 图片中显示的验证码


        此函数用于识别简单字母＋图片验证码，
        返回给图片中显示的验证码
        '''
        ocr = ddddocr.DdddOcr(show_ad=False)
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        print('识别出的验证码为：' + res)
        return res

    def ocr_slide_with_hole(self, bgimg_path, fullpage_path):
        '''
        :param imgpath: 需要识别的背景图片路径
        :param fullpage_path: 需要识别的全图片路径
        :return: 图片中显示的验证码缺口坐标


        此函数用于识别 一张图为带坑位的滑块图，
        返回图片中显示的滑块图缺口坐标
        '''
        slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        with open(bgimg_path, 'rb') as f:
            target_bytes = f.read()
        with open(fullpage_path, 'rb') as f:
            background_bytes = f.read()
        img = cv2.imread(bgimg_path)
        res = slide.slide_comparison(target_bytes, background_bytes)
        print(res)
        return res

    def ocr_slide_with_clean(self, bgimg_path, fullpage_path):
        '''小滑块为单独的png图片，背景是透明图'''
        '''
        :param imgpath: 需要识别的背景图片路径
        :param fullpage_path: 需要识别的全图片路径
        :return: 图片中显示的验证码缺口坐标
        
        
        此函数用于识别 小滑块为单独的png图片，背景是透明图的滑块图，
        返回图片中显示的滑块图缺口坐标
        '''
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        with open(bgimg_path, 'rb') as f:
            target_bytes = f.read()
        with open(fullpage_path, 'rb') as f:
            background_bytes = f.read()
        res = det.slide_match(target_bytes, background_bytes)
        print(res, res.get('target')[0])
        return res

    def ocr_click_choose(self, test_img_path, result_img_path):
        '''
        :param test_img_path: 需要识别的背景图片路径
        :param result_img_path: 识别后，生成的 新的 带红框的 全图片 的路径
        :return: 点选图片中的图案坐标


        此函数用于识别 简单点选验证码 图片，
        返回图片中显示的 点选验证码 所在坐标
        '''
        det = ddddocr.DdddOcr(det=True, show_ad=False)
        with open(test_img_path, 'rb') as f:
            image = f.read()
        poses = det.detection(image)
        print(poses)
        print(poses[0][0], poses[1][0], poses[2][0])
        im = cv2.imread(test_img_path)
        for box in poses:
            x1, y1, x2, y2 = box
            im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        cv2.imwrite(result_img_path, im)
        return poses

    def create_infile(self, name=None):
        '''
        :param name: 需要创建的文件夹的名字
        :return: None


        此函数用于创建一个在 当前文件夹 下的新文件夹，
        名字默认为New_file。可以自行指定
        '''
        if name is None:
            name = 'New_file'
        if not os.path.exists(f'./{name}'):
            os.mkdir(f'./{name}')

    def create_outfile(self, name=None):
        '''
        :param name: 需要创建的文件夹的名字
        :return: None


        此函数用于创建一个在 上一级文件夹 的新文件夹，
        名字默认为New_file。可以自行指定
        '''
        if name is None:
            name = 'New_file'
        if not os.path.exists(f'../{name}'):
            os.mkdir(f'../{name}')

    def create_timestamp(self):
        '''
        :return: 时间戳


        此函数用于创建一个在爬虫任务中经常出现的时间戳
        '''
        return round(time.time() * 1000)

    def create_random_str(self, length=16, pool=None):
        '''
        :param length: 指定需要返回的random_str个数
        :param pool: 指定random_str的pool范围
        :return: random_str


        此函数用于创建一个在爬虫任务中经常出现的 乱序大小写英文字母＋数字 随机字符组合，
        随机字符组合池默认为ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890，可以自行指定，
        随机字符组合位数默认为16位，可以自行指定
        '''
        if pool is None:
            pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        result = ''
        for i in range(length):
            result += random.choice(pool)
        return result

    def get(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送get请求，
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request('get', url, headers=headers, params=params, data=data, **kwargs)

    def options(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送options请求，
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("options", url, headers=headers, data=data, params=params, **kwargs)

    def head(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送head请求
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("head", url, headers=headers, data=data, params=params, **kwargs)

    def post(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送post请求
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("post", url, headers=headers, data=data, json=json, params=params, **kwargs)

    def put(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送put请求
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("put", url, headers=headers, data=data, params=params, **kwargs)

    def patch(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送patch请求
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("patch", url, headers=headers, data=data, params=params, **kwargs)

    def delete(self, url, headers=None, data=None, params=None, **kwargs):
        '''
        :param url: 需要请求的网址
        :param headers: 请求头，如果没有指定，则默认使用FakeUA库进行创建使用
        :param data: 提交表单，如果没有指定，则默认为None
        :param params: 参数，如果没有指定，则默认为None


        此函数用于模拟requests发送delete请求
        但是有默认的请求头，无需在网页上或第三方库中获取
        '''
        if headers is None:
            headers = self.headers
        return requests.request("delete", url, headers=headers, data=data, params=params, **kwargs)

    def re(self, res, str_1, str_2):
        '''
        :param res: 原始内容 或 原始响应
        :param str_1: 第一部分的分割范围
        :param str_2: 第二部分的分割范围
        :return: 分割范围之间的所有字符串


        此函数用于返回一个列表，
        列表中的元素为 第一个 符合给定范围条件 之间的字符串

        使用实例:
        a = 123aaa456bbb456ccc456
        print(spider_tools().re(a,'123','456')) ==> aaa
        '''

        pattern = re.compile(r'{}(.*?){}'.format(re.escape(str_1), re.escape(str_2)))
        values = re.findall(pattern, res)
        return values

    def xpath(self, res, x_path):
        '''
        :param res: 原始HTML字符串
        :param x_path: 根据传入的原始HTML字符串，使用XPATH进行元素定位
        :return: 使用XPATH定位到的网页元素


        此函数用于通过对传入的原始HTML字符串，
        使用XPATH进行元素定位，
        并且返回定位到的元素
        '''
        tree = etree.HTML(res)
        return tree.xpath(x_path)

    def rebuidtext(self, res: str):
        '''
        :param res: 原始HTML字符串
        :return: 重构后的HTML字符串

        此函数用于重构response响应

        常见的打印页面报错如下:
        UnicodeEncodeError: ‘gbk’ codec can’t encode character ‘\xe7’ in position 318: illegal multibyte sequence
        中文翻译为UnicodeEncodeError：‘gbk’编解码器无法在位置318中编码字符’\ xe7’：非法的多字节序列

        很多时候页面返回的response响应无法进行打印输出，
        最常用的方法就是对response进行重构，
        完成后即可打印输出

        值得一提，此方法并不是通解，
        如果调用此函数对response进行重构后，仍然不能打印页面，请另寻办法解决。

        笔者在此列出两条本人常用的解决办法，可供各位参考:
        1、调用此方法对response进行重构;
        2、在Python文件最上方加入如下代码:
            import sys,io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
            #'gb18030'可修改为ISO-8859-1,gb2312。依据具体情况自行更换即可
        '''
        return res.encode('ISO-8859-1').decode('utf8')

    def json_loads(self, data):
        '''
        :param data: 需要由 字符串 反序列化为 JSON 的数据
        :return: 由 字符串 反序列化为 JSON 的数据


        此函数用于将 字符串数据 反序列化为 JSON数据
        '''
        return json.loads(data)

    def json_load(self, data):
        '''
        :param data: 需要由 文件流 反序列化为 JSON 的数据
        :return: 由 文件流 反序列化为 JSON 的数据


        此函数用于将 文件流数据 反序列化为 JSON数据
        '''
        return json.load(data)

    def json_dump(self, data, fp):
        '''
        :param data: 需要由 JSON 反序列化为 字符串 并 进行持久化储存 的数据
        :param fp: 用fp指代的文件对象       example: with open() as fp:
        :return: 由 JSON 反序列化为 字符串 并 进行持久化储存 的数据


        此函数用于将 JSON数据 反序列化为 字符串数据 并对其进行 持久化储存
        '''
        return json.dump(data, fp)

    def json_dumps(self, data):
        '''
        :param data: 需要由 JSON 反序列化为 字符串 的数据
        :return: 由 JSON 反序列化为 字符串 的数据


        此函数用于将 JSON数据 反序列化为 字符串数据
        '''
        return json.dumps(data)

    def create_headers(self):
        '''
        :return: 随机请求头


        此函数用于创建一个随机，常用的请求头
        '''
        return {'User-Agent': UserAgent().random}

    def info(self, msg, *args, **kwargs):
        '''
        :param msg: 需要在控制台输出的数据,输出格式为INFO


        此函数用于在控制台输出的数据,输出格式为INFO
        '''
        logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        '''
        :param msg: 需要在控制台输出的数据,输出格式为DEBUG


        此函数用于在控制台输出的数据,输出格式为DEBUG
        '''
        logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        '''
        :param msg: 需要在控制台输出的数据,输出格式为WARING


        此函数用于在控制台输出的数据,输出格式为WARING
        '''
        logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        '''
        :param msg: 需要在控制台输出的数据,输出格式为ERROE


        此函数用于在控制台输出的数据,输出格式为ERROE
        '''
        logger.error(msg, *args, **kwargs)

    @staticmethod
    def catch_bug(func):
        '''
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
        '''

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"{func.__name__} 抛出异常，异常已捕获，内容如下:\n {e}")

        return wrapper

    @staticmethod
    def test_time(func):
        '''
        :param func: 需要传入的函数
        :return: 传入的原函数所耗费的时间


        此函数用于测试函数运行时间

        使用示例:
                @spidertool.test_time
                def test_func():sleep(2)

                if __name__ == '__main__':
                    test_func ==> test_func 函数在 0m 2s 内完成
        '''

        def target(*args, **kwargs):
            since = time.time()
            result = func()
            time_elapsed = time.time() - since
            print(func.__name__, '函数在 {:.0f}m {:.0f}s 内完成'.format(time_elapsed // 60, time_elapsed % 60))
            return result

        return target()

    @staticmethod
    def retry(max_attempts: int, delay):
        '''
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
        '''

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
                print(f'{func.__name__}异常情况如下\n{exception}')
                raise Exception("已达到所设置的{}次最大重试次数".format(max_attempts))

            return wrapper

        return decorator

    def encrypt_AES(self, data, key, iv, mode='cbc'):
        '''
        :param data: 待加密数据
        :param key: AES算法中的key
        :param iv: AES算法中的iv
        :param mode: AES算法中的加密模式，默认为CBC模式，也可手动指定为EBC模式
        :return: 经过AES算法加密后的数据

        此函数用于还原JS中AES算法,输出格式为base64

        使用示例:
                spidertool.encrypt_AES(data, key, iv)
        '''
        if mode.lower() == 'cbc':
            cipher = AES.new(key, AES.MODE_CBC, iv)
        elif mode.lower() == 'ecb':
            cipher = AES.new(key, AES.MODE_ECB)
        data = data.encode('utf-8')
        if len(data) % 16 != 0:
            data += b' ' * (16 - len(data) % 16)  # Pad the data if necessary
        encrypted_data = cipher.encrypt(data)
        return base64.b64encode(encrypted_data)

    def encrypt_DES(self, data, key, iv):
        '''
        :param data: 待加密数据
        :param key: DES算法中的key
        :param iv: DES算法中的iv
        :return: 经过DES算法加密后的数据

        此函数用于还原JS中AES算法,输出格式为base64

        使用示例:
                spidertool.encrypt_DES(data, key, iv)
        '''
        cipher = DES.new(key, DES.MODE_CBC, iv)
        padded_data = pad(data, DES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data)

    def encrypt_RSA(self, message, pubkey, modulus=10001):
        '''
        :param message: 待加密数据
        :param pubkey: RSA算法中的pubkey
        :param modulus: RSA算法中的模值，默认为10001
        :return: 经过RSA算法加密后的数据

        此函数用于还原JS中RSA算法

        使用实例:
                spidertool.encrypt_RSA(message, pubkey)
        '''
        key = RSA.construct((pubkey, modulus))
        cipher = PKCS1_v1_5.new(key)
        cipher_text = cipher.encrypt(message.encode())
        return cipher_text.hex()

    def encrypt_Base64(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过base64编码转换后的数据

        此函数用于还原JS中base64编码转换

        使用示例:
        spidertool.encrypt_Base64(data)
        '''
        return base64.b64encode(data)

    def encrypt_MD5(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过md5加密后的数据

        此函数用于还原JS中md5算法加密

        使用实例:
        spidertool.encrypt_MD5(data)
        '''
        md5_hash = hashlib.md5()

        data_bytes = data.encode('utf-8')

        md5_hash.update(data_bytes)

        hex_digest = md5_hash.hexdigest()

        return hex_digest

    def encrypt_SHA1(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA1加密后的数据

        此函数用于还原JS中SHA1算法加密

        使用实例:
        spidertool.encrypt_SHA1(data)
        '''
        sha1 = hashlib.sha1()
        sha1.update(data.encode())
        return sha1.hexdigest()

    def encrypt_SHA256(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA256加密后的数据

        此函数用于还原JS中SHA256算法加密

        使用实例:
        spidertool.encrypt_SHA256(data)
        '''
        sha256 = hashlib.sha256()
        sha256.update(data.encode())
        return sha256.hexdigest()

    def encrypt_SHA512(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA512加密后的数据

        此函数用于还原JS中SHA512算法加密

        使用实例:
        spidertool.encrypt_SHA512(data)
        '''
        sha512 = hashlib.sha512()
        sha512.update(data.encode())
        return sha512.hexdigest()

    def encrypt_SHA384(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA384加密后的数据

        此函数用于还原JS中SHA384算法加密

        使用实例:
        spidertool.encrypt_SHA384(data)
        '''
        hash_object = hashlib.sha384(data.encode())
        return hash_object.hexdigest()

    def encrypt_HMAC(self, data, key):
        '''
        :param data: 待加密的数据
        :param key: HMAC加密需要的key
        :return: 经过HMAC加密后的数据

        此函数用于还原JS中HMAC算法加密

        使用实例:
        spidertool.encrypt_HMAC(data, key)
        '''
        h = hmac.new(key, data, digestmod=SHA256)
        return h.digest()

    def encrypt_JWT(self, data, private_key, algorithm='RS256'):
        '''
        :param data: 待加密的数据
        :param private_key: JWT加密需要的private_key
        :param algorithm: 签名算法
        :return: 签名后的JWT

        此函数用于还原JS中JWT算法加密

        使用实例:
        spidertool.encrypt_JWT(data, private_key)
        '''
        # 使用jwt库来生成JWT
        token = jwt.encode(data, private_key, algorithm=algorithm)
        return token

    def encrypt_PBKDF2(self, password, salt, iterations, key_length, hash_algorithm):
        '''
        :param password: 要派生的密码（字节串）。
        :param salt: 随机生成的盐（字节串）。
        :param iterations: 迭代次数，用于增加计算难度。
        :param key_length: 指定派生密钥的长度（以字节为单位）。
        :param hash_algorithm: 用于内部哈希计算的算法，如'sha256'、'sha512'等。
        :return: 派生的密钥（字节串）

        此函数用于还原JS中PBKDF2算法加密,使用PBKDF2算法从密码派生密钥。

        使用示例:
                spidertool.encrypt_PBKDF2(password, salt, iterations, key_length, hash_algorithm)

        '''
        key = PBKDF2(password, salt, dkLen=key_length, count=iterations,
                     prf=lambda p, s: hmac.new(p, s, getattr(hashlib, hash_algorithm)).digest())
        return key