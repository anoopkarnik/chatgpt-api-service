from extensions import db
from datetime import datetime
import pytz

def get_ist_time():
    utc_now = datetime.utcnow()
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    return ist_now

class ChatgptMessage(db.Model):
    __tablename__ = 'chatgpt_messages'
    __table_args__ = {"schema": "chatgpt_schema",'extend_existing': True}

    id = db.Column(db.String(255), primary_key=True)
    user_message = db.Column(db.Text)
    system_instructions = db.Column(db.Text)
    bot_message = db.Column(db.Text)
    completion_tokens = db.Column(db.Integer)
    prompt_tokens = db.Column(db.Integer)
    finish_reason = db.Column(db.String(255))
    model = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=get_ist_time)
    updated_at = db.Column(db.DateTime, default=get_ist_time, onupdate=get_ist_time)
    def __repr__(self):
        return f'<Message {self.id}>'