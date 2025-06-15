# -*- coding: UTF-8 -*-
'''
@Project ：bid_spiders
@File    ：genspider.py
@IDE     ：PyCharm
@Author  ：JOUSKA.
@Date    ：2024-07-15 21:35
'''
import os
import sys
import click
from scrapy.utils.template import render_templatefile

# 获取当前脚本所在目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

class AutoModel:
    # 单一模板文件路径
    ASYNC_REQUEST_TEMPLATE_FILE = os.path.join(f"{parent_dir}/templates", "async_request.tmpl")

    def create_spider_file(
            self,
            spider_name: str,
            class_name: str,
            web_site_name: str,
            output_dir: str  # 新增输出目录参数
    ):
        '''
        使用单一模板生成爬虫文件

        :param spider_name: 爬虫名
        :param class_name: 爬虫类名
        :param web_site_name: 网站名
        :param output_dir: 输出目录
        '''
        # 准备模板变量
        tvars_seed = {
            "name": spider_name,
            "classname": class_name,
            "web_site_name": web_site_name,
        }

        # 构建输出文件路径
        spider_file = os.path.join(output_dir, f"{spider_name}.py")

        # 检查是否已存在同名文件
        if os.path.exists(spider_file):
            click.echo(f"已存在 {spider_file}，跳过生成")
            return

        # 复制模板内容到新文件
        with open(self.ASYNC_REQUEST_TEMPLATE_FILE, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

        with open(spider_file, "w", encoding="utf-8") as output_file:
            output_file.write(template_content)

        # 渲染模板变量
        render_templatefile(spider_file, **tvars_seed)

        click.echo(f"爬虫文件已生成: {spider_file}")


def gen_spider(
        spider_name: str,
        web_site_name: str,
        spider_config: dict = None,  # 保持参数兼容但不再使用
        output_dir: str = None  # 新增输出目录参数
):
    '''
    自动生成爬虫代码

    :param spider_name: 爬虫名
    :param web_site_name: 网站名
    :param spider_config: 配置 (保留但不再使用)
    :param output_dir: 输出目录 (默认为当前目录)
    '''
    auto = AutoModel()

    # 处理输出目录
    if output_dir is None:
        output_dir = os.getcwd()  # 默认为当前工作目录

    # 生成类名 (首字母大写的驼峰命名)
    classname = "".join(word.title() for word in spider_name.split("_"))

    # 创建爬虫文件
    auto.create_spider_file(
        spider_name=spider_name,
        class_name=classname,
        web_site_name=web_site_name,
        output_dir=output_dir
    )


if __name__ == '__main__':
    # 示例调用
    gen_spider(
        spider_name="ztbgl_spider",
        web_site_name="https://www.example.com/",
        output_dir=os.getcwd()  # 输出到当前目录
    )