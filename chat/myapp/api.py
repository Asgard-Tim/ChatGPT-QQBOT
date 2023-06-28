from rest_framework.decorators import api_view
from rest_framework.response import Response
from .openai_key import key
import requests
import re

openai_secret_key = key

messages = []
tokenizer = re.compile(r"\w+")

@api_view(['GET','POST'])
def chat_api(request):
    message = request.GET['msg']
    print(message)
    messages.append({"role": "user", "content": message})
    print(messages)
    
    # 计算 messages 列表中消息的总 token 数
    total_tokens = sum(len(tokenizer.findall(msg["content"])) for msg in messages)
    print(f"Total Tokens: {total_tokens}")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_secret_key}'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_data = response.json()
    text = response_data["choices"][0]
    text1 = response_data["choices"][0]["message"]
    messages.append(text1)
    # 如果总 token 数超过 1024，重置 messages 列表为空
    if total_tokens > 1024:
        messages.clear()
    if message == "再见":
        messages.clear()
    return Response({'text': text})
