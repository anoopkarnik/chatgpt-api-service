from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from main.repositories.MessageRepository import MessageRepository
from main.repositories.ThreadRepository import ThreadRepository
from main.repositories.AssistantRepository import AssistantRepository


logger = logging.getLogger(__name__)

def get_reply_by_assistant(message_body):
    message_repo = MessageRepository()
    thread_repo = ThreadRepository()
    assistant_repo = AssistantRepository()
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_api_key)
    logger.info(f'OpenAI client created')
    assitant_name = message_body['assistant_name']
    assistant_id = os.environ.get(assitant_name)
    assistant_object = client.beta.assistants.retrieve(assistant_id)
    assistant_model = assistant_repo.get_assistant_by_id(assistant_id)
    if assistant_model is None:
        assistant_model = assistant_repo.create_assistant(assistant_id,assistant_object.name)
        logger.info(f'Assistant object: {assistant_object.name} loaded')
    if message_body['thread'] == "new":
        thread = client.beta.threads.create()
        logger.info(f'Thread created: {thread.id}')
        thread_model = thread_repo.create_thread(thread.id,assistant_id)
        thread_id = thread.id
    else:
        threads = thread_repo.get_all_threads()
        thread_id = threads[0].thread_id
    message_object = client.beta.threads.messages.create(thread_id =thread_id, role='user',content =message_body['message'])
    logger.info(f'Message created: {message_object.id}')
    run = client.beta.threads.runs.create(thread_id = thread_id,assistant_id = assistant_id)
    logger.info(f'Run created: {run.id} and in {run.status} status')
    start = 0 
    while run.status != 'completed':
        time.sleep(4)
        run = client.beta.threads.runs.retrieve(thread_id = thread_id,run_id = run.id)
        logger.info(f'Run {run.id} is in {run.status} status')
        start += 1
        if start > 30:
            logger.info(f'Stopped waiting for run {run.id} to complete')
            break
    messages = client.beta.threads.messages.list(thread_id = thread_id).json()
    message_result = json.loads(messages)
    thread_id = message_result['data'][0]['thread_id']
    logger.info(f'Messages retrieved: {message_result}')
    bot_message = '/n'.join([message['text']['value'] for message in message_result['data'][0]['content']])
    message_model = message_repo.create_message(
        message_result['data'][1]['id'],
        message_result['data'][0]['id'],
        message_body['message'],
        bot_message,
        thread_id,
        assistant_id)
    return {
        'thread_id': thread_id,
        'message': bot_message,
        'assistant_id': assistant_id,
    }