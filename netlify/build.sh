#!/bin/bash

# 创建函数库目录
mkdir -p .netlify/functions/lib

# 安装 Python 依赖到函数库目录
pip install -r requirements.txt -t .netlify/functions/lib

# 复制源代码到函数库目录
mkdir -p .netlify/functions/lib/src
cp -r src/* .netlify/functions/lib/src/

# 显示安装的依赖
echo "已安装的依赖:"
ls -la .netlify/functions/lib

# 显示复制的源代码
echo "复制的源代码:"
ls -la .netlify/functions/lib/src

echo "构建完成!" 