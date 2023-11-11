from openai import OpenAI
import os
import logging
import requests
import time
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import uuid

logger = logging.getLogger(__name__)

def create_text_to_speech(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    response = client.audio.speech.create(
        model='tts-1',
        voice='nova',
        input=message_body['message'],
    )
    logger.info(f'Speech created: {response}')
    if 'output_path' in message_body:
        output_path = message_body['output_path']
    else:
        output_path = 'data'
    if 'file_name' in message_body:
        file_name = message_body['file_name']
    else:
        file_name = f'{uuid.uuid4()}.mp3'
    response.stream_to_file(os.path.join(output_path,file_name))
    audio = AudioSegment.from_mp3(os.path.join(output_path,file_name))
    play(audio)

def create_speech_to_text(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    audio_file = open(message_body['path'], 'rb')
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
    )
    return json.loads(transcript.json())

def translate_speech_to_text(message_body):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    audio_file = open(message_body['path'], 'rb')
    transcript = client.audio.translations.create(
        model='whisper-1',
        file=audio_file,
    )
    return json.loads(transcript.json())
