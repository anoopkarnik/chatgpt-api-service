from main.models.Assistant import Message
from fuzzywuzzy import fuzz
from extensions import db


class MessageRepository:
    def __init__(self):
        self.model = Message

    def get_all_messages(self):
        return self.model.query.all()
    
    def get_message_by_user_message_id(self, user_message_id):
        return self.model.query.filter_by(user_message_id=user_message_id).first()

    def get_message_by_bot_message_id(self, bot_message_id):
        return self.model.query.filter_by(bot_message_id=bot_message_id).first()

    def get_message_by_thread_id(self, thread_id):
        return self.model.query.filter_by(thread_id=thread_id).first()

    def get_message_by_assistant_id(self, assistant_id):
        return self.model.query.filter_by(assistant_id=assistant_id).first()

    def create_message(self, user_message_id, bot_message_id, user_message, bot_message, thread_id, assistant_id):
        new_message = self.model(user_message_id=user_message_id,bot_message_id=bot_message_id,user_message=user_message,bot_message=bot_message,thread_id=thread_id,assistant_id=assistant_id)
        db.session.add(new_message)
        db.session.commit()
        return new_message
    
    def update_message(self, user_message_id, bot_message_id, user_message, bot_message, thread_id, assistant_id):
        message = self.get_message_by_user_message_id(user_message_id)
        message.bot_message_id = bot_message_id
        message.user_message = user_message
        message.bot_message = bot_message
        message.thread_id = thread_id
        message.assistant_id = assistant_id
        db.session.commit()
        return message

    def delete_message(self, user_message_id):
        message = self.get_message_by_user_message_id(user_message_id)
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

    