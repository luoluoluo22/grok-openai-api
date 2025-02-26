#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import uuid
import time
import logging
import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Grok API配置
GROK_URL = "https://grok.com/rest/app-chat/conversations/{conversation_id}/responses"
DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://grok.com",
    "referer": "https://grok.com/chat/{conversation_id}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# 固定的会话ID，避免每次创建新的会话
FIXED_CONVERSATION_ID = "d74ca9d9-5fd3-4e9b-9acc-5635539dcc2d"

# 请求频率限制处理
last_request_time = 0
MIN_REQUEST_INTERVAL = 5  # 最小请求间隔（秒）

def get_grok_response(prompt, conversation_id=None, parent_id=None, stream=False, headers=None, max_retries=3, cookie=None):
    """
    调用Grok API获取响应，带重试机制
    """
    global last_request_time
    
    # 检查请求频率
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    
    if time_since_last_request < MIN_REQUEST_INTERVAL:
        # 等待足够的时间
        sleep_time = MIN_REQUEST_INTERVAL - time_since_last_request
        logger.info(f"等待 {sleep_time:.2f} 秒以避免请求频率限制...")
        time.sleep(sleep_time)
    
    if not conversation_id:
        conversation_id = FIXED_CONVERSATION_ID
    
    if not headers:
        headers = DEFAULT_HEADERS.copy()
        # 添加认证信息
        headers["cookie"] = cookie or os.environ.get("GROK_COOKIE", "")
        # 更新referer
        headers["referer"] = f"https://grok.com/chat/{conversation_id}"
    
    url = GROK_URL.format(conversation_id=conversation_id)
    
    data = {
        "message": prompt,
        "modelName": "grok-3",
        "parentResponseId": parent_id if parent_id else "938a834c-85ff-4803-a60a-749fe6942784",
        "disableSearch": False,
        "enableImageGeneration": True,
        "imageAttachments": [],
        "returnImageBytes": False,
        "returnRawGrokInXaiRequest": False,
        "fileAttachments": [],
        "enableImageStreaming": True,
        "imageGenerationCount": 2,
        "forceConcise": False,
        "toolOverrides": {},
        "enableSideBySide": True,
        "sendFinalMetadata": True,
        "customInstructions": "",
        "deepsearchPreset": "",
        "isReasoning": False
    }
    
    # 重试机制
    for attempt in range(max_retries):
        try:
            logger.info(f"发送请求到Grok API (尝试 {attempt+1}/{max_retries})...")
            response = requests.post(url, headers=headers, json=data, stream=True)
            
            # 更新最后请求时间
            last_request_time = time.time()
            
            if response.status_code == 429:
                # 请求频率限制
                retry_after = int(response.headers.get('Retry-After', 5))
                logger.warning(f"请求频率限制，等待 {retry_after} 秒后重试...")
                time.sleep(retry_after)
                continue
            
            if response.status_code != 200:
                logger.error(f"Grok API请求失败: {response.status_code}")
                if attempt < max_retries - 1:
                    # 指数退避
                    sleep_time = 2 ** attempt
                    logger.info(f"等待 {sleep_time} 秒后重试...")
                    time.sleep(sleep_time)
                    continue
                raise Exception(f"Grok API请求失败: {response.status_code}")
            
            return response, conversation_id
        
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            if attempt < max_retries - 1:
                # 指数退避
                sleep_time = 2 ** attempt
                logger.info(f"等待 {sleep_time} 秒后重试...")
                time.sleep(sleep_time)
            else:
                raise
    
    raise Exception("达到最大重试次数，请求失败")

def parse_grok_streaming_response(response, sessions=None):
    """
    解析Grok流式响应
    """
    buffer = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                line = chunk.decode('utf-8')
                json_obj = json.loads(line)
                result = json_obj.get("result", {})
                
                if "token" in result:
                    token = result["token"]
                    buffer += token
                    
                    # 构造OpenAI格式的流式响应
                    openai_chunk = {
                        "id": f"chatcmpl-{uuid.uuid4()}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": "grok-3",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {
                                    "content": token
                                },
                                "finish_reason": None
                            }
                        ]
                    }
                    
                    yield f"data: {json.dumps(openai_chunk)}\n\n"
                
                # 处理完成信号
                if "modelResponse" in result and result.get("done", False):
                    # 保存parent_id用于下一次请求
                    if sessions and "id" in result.get("modelResponse", {}):
                        parent_id = result["modelResponse"]["id"]
                        sessions[FIXED_CONVERSATION_ID] = {'parent_id': parent_id}
                        logger.info(f"更新会话ID: {FIXED_CONVERSATION_ID}, parent_id: {parent_id}")
                    
                    # 发送完成信号
                    openai_chunk = {
                        "id": f"chatcmpl-{uuid.uuid4()}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": "grok-3",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {},
                                "finish_reason": "stop"
                            }
                        ]
                    }
                    
                    yield f"data: {json.dumps(openai_chunk)}\n\n"
                    yield "data: [DONE]\n\n"
                    break
                    
            except json.JSONDecodeError:
                continue
    
    # 如果没有正常结束，发送一个完成信号
    if not buffer.endswith("[DONE]"):
        openai_chunk = {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "grok-3",
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }
            ]
        }
        
        yield f"data: {json.dumps(openai_chunk)}\n\n"
        yield "data: [DONE]\n\n"

def parse_grok_response(response, sessions=None):
    """
    解析Grok非流式响应
    """
    full_message = ""
    parent_id = None
    response_text = response.content.decode('utf-8')
    
    for line in response_text.splitlines():
        if line.strip():
            try:
                json_obj = json.loads(line)
                result = json_obj.get("result", {})
                
                # 从token中提取回答
                if "token" in result:
                    full_message += result["token"]
                
                # 从modelResponse中提取最终完整回答（如果存在）
                if "modelResponse" in result and "message" in result["modelResponse"]:
                    full_message = result["modelResponse"]["message"]
                    
                    # 保存parent_id用于下一次请求
                    if "id" in result["modelResponse"]:
                        parent_id = result["modelResponse"]["id"]
            except json.JSONDecodeError:
                continue
    
    # 更新会话信息
    if sessions and parent_id:
        sessions[FIXED_CONVERSATION_ID] = {'parent_id': parent_id}
        logger.info(f"更新会话ID: {FIXED_CONVERSATION_ID}, parent_id: {parent_id}")
    
    return full_message 