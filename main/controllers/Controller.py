from flask import Blueprint, request, jsonify
from main.services.assistants import get_reply_by_assistant
from main.services.audio import create_text_to_speech,create_speech_to_text,translate_speech_to_text
from main.services.chat import chat_with_gpt
from main.services.image import generate_image_by_prompt,generate_image_variations,get_vision_description
import logging

logger = logging.getLogger(__name__)

payload_controller = Blueprint("payload_controller",__name__)

@payload_controller.route("/",methods=["GET"])
def health_check():
	return jsonify({"status":"success"})

@payload_controller.route("/chat_with_assistant",methods=["POST"])
def chat_with_assistant():
	message_body = request.json
	result = get_reply_by_assistant(message_body)
	return jsonify(result)

@payload_controller.route("/text_to_speech",methods=["POST"])
def text_to_speech():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	create_text_to_speech(message_body)
	return jsonify({'result':"success"})

@payload_controller.route("/speech_to_text",methods=["POST"])
def speech_to_text():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	transcript = create_speech_to_text(message_body)
	return jsonify(transcript)

@payload_controller.route("/translate",methods=["POST"])
def translate():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	transcript = translate_speech_to_text(message_body)
	return jsonify(transcript)

@payload_controller.route("/chat",methods=["POST"])
def chat():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	result = chat_with_gpt(message_body)
	return jsonify(result)

@payload_controller.route("/generate_image",methods=["POST"])
def generate_image():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	result = generate_image_by_prompt(message_body)
	return jsonify(result)

@payload_controller.route("/generate_image_variations",methods=["POST"])
def generate_image_variations():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	result = generate_image_variations(message_body)
	return jsonify(result)

@payload_controller.route("/get_vision_description",methods=["POST"])
def get_vision_description():
	logger.info(f'Request received: {request.json}')
	message_body = request.json
	result = get_vision_description(message_body)
	return jsonify(result)