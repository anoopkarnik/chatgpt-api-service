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
import uuid
import boto3
from main.utils.s3 import upload_to_s3,read_from_s3
from main.repositories.AudioRepository import AudioRepository

logger = logging.getLogger(__name__)

def create_text_to_speech(message_body):
    audio_repo = AudioRepository()
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    location_path = message_body['location_path']
    location_type = message_body.get('location_type','s3')
    voice = message_body.get('voice','nova')
    model = message_body.get('model','tts-1')
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=message_body['message'],
    )
    logger.info(f'Speech created: {response}')
    id = uuid.uuid4()
    file_name = f'{id}.mp3'
    location_path = os.path.join(location_path,file_name)
    response.stream_to_file(os.path.join('data',file_name))
    logger.info(f'Speech saved to: {os.path.join("data",file_name)}')
    audio_model = audio_repo.create_audio(id,message_body['message'],location_type,location_path,'text_to_speech',
                                          voice,model)
    if location_type == 's3':
        bucket_name = os.environ.get('VOICE_RECORDINGS_S3_BUCKET_NAME')
        upload_to_s3(os.path.join("data",file_name),location_path,bucket_name)
    audio = AudioSegment.from_mp3(os.path.join("data",file_name))
    play(audio)

def create_speech_to_text(message_body):
    audio_repo = AudioRepository()
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    location_path = message_body['location_path']
    location_type = message_body.get('location_type','s3')
    voice = message_body.get('voice','not applicable')
    model = message_body.get('model','whisper-1')
    id = uuid.uuid4()
    if location_type == 'local':
        audio_file = open(location_path, 'rb')
    else:
        bucket_name = os.environ.get('VOICE_RECORDINGS_S3_BUCKET_NAME')
        audio_file =read_from_s3(location_path,bucket_name)
    transcript = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
    )
    logger.info(f'Transcript created: {transcript}')
    result = json.loads(transcript.json())
    audio_model = audio_repo.create_audio(id,result['text'],location_type,
                                          location_path,'speech_to_text',voice,model)
    return result

def translate_speech_to_text(message_body):
    audio_repo = AudioRepository()
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    logger.info(f'OpenAI client created')
    location_path = message_body['location_path']
    location_type = message_body.get('location_type','s3')
    voice = message_body.get('voice','not applicable')
    model = message_body.get('model','whisper-1')
    id = uuid.uuid4()
    if location_type == 'local':
        audio_file = open(location_path, 'rb')
    else:
        bucket_name = os.environ.get('VOICE_RECORDINGS_S3_BUCKET_NAME')
        audio_file =read_from_s3(location_path,bucket_name)
    transcript = client.audio.translations.create(
        model=model,
        file=audio_file,
    )
    logger.info(f'Translation created: {transcript}')
    result = json.loads(transcript.json())
    audio_model = audio_repo.create_audio(id,result['text'],location_type,
                                          location_path,'translate_speech_to_text',voice,model)
    return result

