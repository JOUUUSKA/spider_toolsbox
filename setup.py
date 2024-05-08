# -*- coding: UTF-8 -*-
'''
@Project ：SpiderToolBox 
@File    ：setup.py
@IDE     ：PyCharm 
@Author  ：JOUSKA.
@Date    ：2024-05-07 20:16 
'''
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Spider_ToolsBox",
    version="0.0.7",
    author="JOUUUSKA",
    author_email="1393827820@qq.com",
    description="Package For Crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JOUUUSKA/SpiderToolBox.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'opencv-python', 'ddddocr', 'execjs', 'fake_useragent', 'loguru', 'lxml']
)
