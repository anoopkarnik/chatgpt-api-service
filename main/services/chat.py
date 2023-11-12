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
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
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
        )
    else:
        response = client.chat.completions.create(
        model = model,
        messages=[
            {"role":"system","content":system_instructions},
            {"role":"user","content":message}
        ]
        )
    logger.info(f'Chat response created: {response.choices[0].message}')
    return json.loads(response.choices[0].message)