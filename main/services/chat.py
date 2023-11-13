from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

def chat_with_gpt(message_body):
    client = OpenAI(api_key="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")
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
    return json.loads(response)['choices'][0]['message']

chat_with_gpt({'message':'Hello, how are you?','system_instructions':'You are a helpful assistant'})