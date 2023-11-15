from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from main.repositories.ChatgptMessageRepository import ChatgptMessageRepository

logger = logging.getLogger(__name__)

def chat_with_gpt(message_body):
    chatgpt_message_repo = ChatgptMessageRepository()
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_api_key)
    logger.info(f'OpenAI client created')
    model = message_body.get('model','gpt-4-1106-preview')
    message = message_body['message']
    system_instructions = message_body.get('system_instructions','You are a helpful assistant')
    if 'format' in message_body:
        format = message_body['format']
        response = client.chat.completions.create(
            model = model,
            response_format={"type":format},
            messages=[
                {"role":"system","content":system_instructions},
                {"role":"user","content":message}
            ]
        ).json()
    else:
        response = client.chat.completions.create(
        model = model,
        messages=[
            {"role":"system","content":system_instructions},
            {"role":"user","content":message}
        ]
        ).json()
    
    # print(json.loads(response)['choices'][0]['message']['content'])
    logger.info(f'Chat response created: {response}')
    result = json.loads(response)
    chatgpt_model = chatgpt_message_repo.create_message(result['id'],message,system_instructions,result['choices'][0]['message']['content'],
                                                            result['usage']['completion_tokens'],result['usage']['prompt_tokens'],
                                                            result['choices'][0]['finish_reason'],result['model'])
    return json.loads(response)

# chat_with_gpt({'message':'Hello, how are you?','system_instructions':'You are a helpful assistant'})