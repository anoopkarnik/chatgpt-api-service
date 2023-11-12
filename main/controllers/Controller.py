from flask import Blueprint, request, jsonify
from main.services.assistants import get_reply_by_assistant
from main.services.audio import create_text_to_speech,create_speech_to_text,translate_speech_to_text
import logging

logger = logging.getLogger(__name__)

payload_controller = Blueprint("payload_controller",__name__)

@payload_controller.route("/",methods=["GET"])
def health_check():
	return jsonify({"status":"success"})

@payload_controller.route("/chat",methods=["POST"])
def chat_with_assistant():
	message_body = request.json
	result = get_reply(message_body)
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