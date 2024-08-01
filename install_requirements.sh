#!/bin/bash

# 确保 poetry 已经安装
if ! command -v poetry &> /dev/null
then
    echo "poetry could not be found, please install it."
    exit 1
fi

# 检查 requirements.txt 文件是否存在
if [ ! -f requirements.txt ]; then
    echo "requirements.txt file not found."
    exit 1
fi

# 读取 requirements.txt 文件并添加依赖
while IFS= read -r line
do
    # 分割依赖项和版本号
    IFS='==' read -r package version <<< "$line"
    if [[ -n $version ]]; then
        # 如果有版本号，则添加带有版本号的依赖
        poetry add "$package==$version"
    else
        # 如果没有版本号，则只添加依赖项名称
        poetry add "$package"
    fi
done < requirements.txt