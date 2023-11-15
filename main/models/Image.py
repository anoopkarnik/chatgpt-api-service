from extensions import db
from datetime import datetime
import pytz

def get_ist_time():
    utc_now = datetime.utcnow()
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    return ist_now

class Image(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {"schema": "chatgpt_schema",'extend_existing': True}

    id = db.Column(db.String(255), primary_key=True)
    message = db.Column(db.Text)
    location_type = db.Column(db.Text)
    location_path = db.Column(db.String(255))
    function_type = db.Column(db.String(255))
    voice = db.Column(db.String(255))
    model = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=get_ist_time)
    updated_at = db.Column(db.DateTime, default=get_ist_time, onupdate=get_ist_time)
    
    def __repr__(self):
        return f'<Message {self.message_id}>'