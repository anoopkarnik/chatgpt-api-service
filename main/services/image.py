from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import boto3

logger = logging.getLogger(__name__)

def generate_image_by_prompt(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    response = client.images.generate(
        model="dall-e-3",
        prompt=message_body['prompt'],
        size="1024x1024",
        quality="standard",
        n=1
    )
    logger.info(f'Image created: {response.data[0].url}')
    # print(response)
    return response.data[0]

def generate_image_variations(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    variations = message_body.get('n',2)
    response = client.images.create_variation(
        image=open(message_body['image_path'], "rb"),
        n=variations,
        size='1024x1024'
    )
    logger.info(f'Image created: {response.data}')
    return response.data

def get_vision_description(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    messages =[]
    message = {}
    message['role'] = 'user'
    contents = []
    contents.append({'type':'text','text':message_body['prompt']})
    for url in message_body['urls']:
        contents.append({'type':'image_url','image_url':{'url':url}})
    message['content'] = contents
    messages.append(message)
    response = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=messages,
        max_tokens=300
    )
    logger.info(f'Image description created: {response.choices[0]}')
    # print(response)
    return response.choices[0]

# get_vision_description({'prompt':'from the cheatsheets give me the list of al commands with headings and subheadings in json format.','urls':['https://miro.medium.com/v2/resize:fit:2000/1*PyqDkHpHdzqC-p1AKcW4Ew.png']})
# generate_image_variations({'image_path':'/home/anoop/Downloads/1.png','n':2})
# generate_image_by_prompt({'prompt':'give me cheatsheets of docker'})