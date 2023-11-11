from flask import Blueprint, request, jsonify
from main.services.assistants import get_reply

payload_controller = Blueprint("payload_controller",__name__)

@payload_controller.route("/",methods=["GET"])
def health_check():
	return jsonify({"status":"success"})

@payload_controller.route("/chat",methods=["POST"])
def chat_with_assistant():
	message_body = request.json
	result = get_reply(message_body)
	return jsonify(result)