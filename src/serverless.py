#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
import uuid
import time
import traceback
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

try:
    # 导入API模块
    from src.api.grok_api import (
        get_grok_response, 
        parse_grok_response,
        FIXED_CONVERSATION_ID
    )
except ImportError as e:
    logger.error(f"导入错误: {str(e)}")
    logger.error(f"Python路径: {sys.path}")
    logger.error(f"当前目录: {os.getcwd()}")
    logger.error(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")
    logger.error(f"堆栈跟踪: {traceback.format_exc()}")

# 存储会话信息（注意：在无服务器环境中，这个会在每次请求后重置）
sessions = {}

def handle_models_request():
    """
    处理模型列表请求
    """
    models = [
        {
            "id": "grok-3",
            "object": "model",
            "created": int(time.time()),
            "owned_by": "grok"
        }
    ]
    
    return {
        "statusCode": 200,
        "body": json.dumps({"object": "list", "data": models}),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def handle_chat_completions_request(body):
    """
    处理聊天完成请求
    """
    try:
        data = json.loads(body) if body else {}
        logger.info(f"收到请求: {data}")
        
        # 提取参数
        messages = data.get('messages', [])
        stream = data.get('stream', False)
        
        # 从消息中提取最后一条用户消息作为prompt
        prompt = ""
        for msg in messages:
            if msg.get('role') == 'user':
                prompt = msg.get('content', '')
        
        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "没有找到用户消息"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # 获取会话ID和parent_id
        conversation_id = FIXED_CONVERSATION_ID
        parent_id = None
        
        if conversation_id in sessions:
            parent_id = sessions[conversation_id].get('parent_id')
            logger.info(f"使用现有会话: {conversation_id}, parent_id: {parent_id}")
        else:
            logger.info(f"创建新会话: {conversation_id}")
        
        # 获取cookie
        cookie = os.environ.get("GROK_COOKIE", "")
        
        # 调用Grok API
        grok_response, conversation_id = get_grok_response(
            prompt=prompt,
            conversation_id=conversation_id,
            parent_id=parent_id,
            stream=False,  # 无服务器环境不支持流式响应
            cookie=cookie
        )
        
        # 非流式响应
        content = parse_grok_response(grok_response, sessions)
        
        # 构造OpenAI格式的响应
        response_data = {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "grok-3",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt),
                "completion_tokens": len(content),
                "total_tokens": len(prompt) + len(content)
            },
            "conversation_id": conversation_id
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(response_data),
            "headers": {"Content-Type": "application/json"}
        }
    
    except Exception as e:
        logger.exception(f"处理请求时出错: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            }),
            "headers": {"Content-Type": "application/json"}
        }

def handle_index_request():
    """
    处理首页请求
    """
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "message": "Grok OpenAI API 服务正在运行",
            "version": "1.0.0",
            "endpoints": {
                "models": "/v1/models",
                "chat_completions": "/v1/chat/completions"
            }
        }),
        "headers": {"Content-Type": "application/json"}
    }

def main():
    """
    主函数，处理来自Netlify Functions的请求
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
        
        try:
            headers = json.loads(headers_str)
        except json.JSONDecodeError:
            logger.error(f"无法解析头信息: {headers_str}")
            headers = {}
        
        logger.info(f"收到请求: {method} {path}")
        logger.info(f"请求体: {body[:100]}...")
        logger.info(f"头信息: {json.dumps(headers)[:100]}...")
        
        # 规范化路径
        if path.endswith('/'):
            path = path[:-1]
        
        # 根据路径和方法处理请求
        if path == "/v1/models" and method == "GET":
            response = handle_models_request()
        elif path == "/v1/chat/completions" and method == "POST":
            response = handle_chat_completions_request(body)
        elif path == "/" or path == "":
            response = handle_index_request()
        else:
            response = {
                "statusCode": 404,
                "body": json.dumps({"error": "Not Found", "path": path, "method": method}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # 输出响应
        print(json.dumps(response))
    
    except Exception as e:
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