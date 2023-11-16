from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import boto3
import uuid
from main.utils.s3 import upload_to_s3,read_from_s3
from main.repositories.ImageRepository import ImageRepository

logger = logging.getLogger(__name__)

def generate_image_by_prompt(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    image_repo = ImageRepository()
    logger.info(f'OpenAI client created')
    location_path = message_body.get('location_path','')
    location_type = message_body.get('location_type','url')
    model = message_body.get('model','dall-e-3')
    prompt = message_body['prompt']
    image_size=message_body.get('image_size','1024x1024')
    quality=message_body.get('quality','standard')
    style = message_body.get('style','natural')
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=image_size,
        quality=quality,
        style=style,
        n=1
    )
    logger.info(f'Image created: {response.data[0].json()}')
    # print(response)
    id = uuid.uuid4()
    data = json.loads(response.data[0].json())
    image_model = image_repo.create_image(id,prompt,data['revised_prompt'],location_type,data['url'],
                                          'image_generation',image_size,model,quality,1,style)
    return data

def get_vision_description(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    image_repo = ImageRepository()
    logger.info(f'OpenAI client created')
    location_path = ' | '.join(message_body['urls'])
    location_type = message_body.get('location_type','url')
    model = message_body.get('model','dall-e-3')
    prompt = message_body['prompt']
    max_tokens = message_body.get('max_tokens',300)
    detail = message_body.get('detail','low')
    messages =[]
    message = {}
    message['role'] = 'user'
    contents = []
    contents.append({'type':'text','text':prompt})
    for url in message_body['urls']:
        contents.append({'type':'image_url','image_url':{'url':url,'detail':detail}})
    message['content'] = contents
    messages.append(message)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    result = json.loads(response.json())
    id = uuid.uuid4()
    image_model = image_repo.create_image(id,prompt,'',location_type,location_path,
                                          'image_description',max_tokens,model,detail,1,'')
    logger.info(f'Image description created: {response}')
    # print(response)
    return result
