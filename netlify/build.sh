#!/bin/bash

# 显示当前目录
echo "当前目录: $(pwd)"

# 创建函数库目录
mkdir -p .netlify/functions/lib
echo "创建函数库目录: .netlify/functions/lib"

# 安装 Python 依赖到函数库目录
echo "安装 Python 依赖..."
pip install -r requirements.txt -t .netlify/functions/lib

# 复制源代码到函数库目录
echo "复制源代码..."
mkdir -p .netlify/functions/lib/src
cp -r src/* .netlify/functions/lib/src/

# 复制 serverless.py 到多个位置以确保能找到
echo "复制 serverless.py 到多个位置..."
cp src/serverless.py .netlify/functions/
cp src/serverless.py .netlify/functions/lib/
cp src/serverless.py .netlify/functions/api/serverless.py || mkdir -p .netlify/functions/api && cp src/serverless.py .netlify/functions/api/

# 复制备份 serverless.py 文件
echo "复制备份 serverless.py 文件..."
cp netlify/functions/serverless.py .netlify/functions/
cp netlify/functions/serverless.py .netlify/functions/lib/
cp netlify/functions/serverless.py .netlify/functions/api/ || mkdir -p .netlify/functions/api && cp netlify/functions/serverless.py .netlify/functions/api/

# 确保文件有执行权限
echo "设置执行权限..."
chmod +x .netlify/functions/serverless.py
chmod +x .netlify/functions/lib/serverless.py
chmod +x .netlify/functions/api/serverless.py

# 显示安装的依赖
echo "已安装的依赖:"
ls -la .netlify/functions/lib

# 显示复制的源代码
echo "复制的源代码:"
ls -la .netlify/functions/lib/src

# 显示函数目录
echo "函数目录内容:"
ls -la .netlify/functions/

echo "构建完成!" 