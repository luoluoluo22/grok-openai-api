#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import uuid
import time
import logging
from flask import Flask, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv

from api.grok_api import (
    get_grok_response, 
    parse_grok_streaming_response, 
    parse_grok_response,
    FIXED_CONVERSATION_ID
)

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 存储会话信息
sessions = {}

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """
    OpenAI兼容的聊天完成API
    """
    try:
        data = request.json
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
            return jsonify({"error": "没有找到用户消息"}), 400
        
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
            stream=stream,
            cookie=cookie
        )
        
        if stream:
            # 流式响应
            def generate():
                for chunk in parse_grok_streaming_response(grok_response, sessions):
                    yield chunk
            
            return Response(
                stream_with_context(generate()),
                content_type='text/event-stream'
            )
        else:
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
            
            return jsonify(response_data)
    
    except Exception as e:
        logger.exception(f"处理请求时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/v1/models', methods=['GET'])
def list_models():
    """
    OpenAI兼容的模型列表API
    """
    models = [
        {
            "id": "grok-3",
            "object": "model",
            "created": int(time.time()),
            "owned_by": "grok"
        }
    ]
    
    return jsonify({"object": "list", "data": models})

@app.route('/', methods=['GET'])
def index():
    """
    首页
    """
    return jsonify({
        "status": "ok",
        "message": "Grok OpenAI API 服务正在运行",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat_completions": "/v1/chat/completions"
        }
    })

if __name__ == '__main__':
    # 启动服务
    logger.info("启动Grok OpenAI API服务...")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False) 