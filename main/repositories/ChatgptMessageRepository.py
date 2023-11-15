from main.models.Chatgpt import ChatgptMessage
from fuzzywuzzy import fuzz
from extensions import db

class ChatgptMessageRepository:
    def __init__(self):
        self.model = ChatgptMessage

    def get_all_messages(self):
        return self.model.query.all()
    def get_message_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
    def create_message(self, id, user_message, system_instructions, bot_message, completion_tokens, prompt_tokens, finish_reason,model):
        new_message = self.model(id=id,user_message=user_message,system_instructions=system_instructions,
                                 bot_message=bot_message,completion_tokens=completion_tokens,prompt_tokens=prompt_tokens,
                                 finish_reason=finish_reason,model=model)
        db.session.add(new_message)
        db.session.commit()
        return new_message
    def update_message(self, id, user_message, system_instructions, bot_message, completion_tokens, prompt_tokens, finish_reason,model):
        message = self.get_message_by_id(id)
        message.user_message = user_message
        message.system_instructions = system_instructions
        message.bot_message = bot_message
        message.completion_tokens = completion_tokens
        message.prompt_tokens = prompt_tokens
        message.finish_reason = finish_reason
        message.model = model
        db.session.add(message)
        db.session.commit()
        return message
    def delete_message(self, id):
        message = self.get_message_by_id(id)
        db.session.delete(message)
        db.session.commit()
        return message
    def get_message_by_user_message(self, user_message):
        messages = self.get_all_messages()
        for message in messages:
            if fuzz.ratio(message.user_message, user_message) > 50:
                return message
        return None
    def get_message_by_bot_message(self, bot_message):
        messages = self.get_all_messages()
        for message in messages:
            if fuzz.ratio(message.bot_message, bot_message) > 50:
                return message
        return None