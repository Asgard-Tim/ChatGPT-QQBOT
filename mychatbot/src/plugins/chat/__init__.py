import json
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.adapters import Event
import requests
import re
import urllib.parse

pattern = re.compile(r"(.*)")  # 匹配任意消息内容

chatgpt = on_message(rule=to_me(), priority=10, block=True)


@chatgpt.handle()
async def handle_function(event: Event):
    message = event.get_plaintext()
    
    if message:
        match = pattern.match(message.strip())
        if not match:
            # 如果匹配失败则结束命令处理
            await chatgpt.finish("请输入内容")
            return
        query = match.group(1)  # 获取正则匹配结果中第一个括号中的内容
        text = requestApi(query)
        print(text)
        await chatgpt.finish(text)


def requestApi(msg):
    msg_body = {
        "msg": msg
    }
    encoded_msg = urllib.parse.quote(msg)  # 对消息内容进行URL编码
    response = requests.get('http://127.0.0.1:8000/chat-api/?msg=' + encoded_msg)
    result = json.loads(response.text)
    text = result['text']['message']['content']
    return text
