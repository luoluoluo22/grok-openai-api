#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    简单的备份处理函数
    """
    try:
        # 获取命令行参数
        if len(sys.argv) < 5:
            logger.error("参数不足")
            print(json.dumps({
                "statusCode": 500,
                "body": json.dumps({"error": "参数不足"}),
                "headers": {"Content-Type": "application/json"}
            }))
            return
        
        method = sys.argv[1]
        path = sys.argv[2]
        body = sys.argv[3]
        headers_str = sys.argv[4]
        
        # 记录环境信息
        logger.info(f"Python 版本: {sys.version}")
        logger.info(f"Python 路径: {sys.path}")
        logger.info(f"当前目录: {os.getcwd()}")
        logger.info(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")
        logger.info(f"环境变量: {dict(os.environ)}")
        
        # 返回简单响应
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "status": "ok",
                "message": "备份 serverless.py 正在运行",
                "version": "1.0.0",
                "path": path,
                "method": method,
                "headers": headers_str[:100] + "...",
                "body": body[:100] + "..." if len(body) > 100 else body
            }),
            "headers": {"Content-Type": "application/json"}
        }
        
        # 输出响应
        print(json.dumps(response))
    
    except Exception as e:
        import traceback
        logger.exception(f"处理请求时出错: {str(e)}")
        error_response = {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            }),
            "headers": {"Content-Type": "application/json"}
        }
        print(json.dumps(error_response))

if __name__ == "__main__":
    main() 