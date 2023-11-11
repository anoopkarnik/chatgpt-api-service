from extensions import db

class Assistant(db.Model):
    __tablename__ = 'assistants'
    __table_args__ = {"schema": "chatgpt_schema"}

    assistant_id = db.Column(db.String(255), primary_key=True)
    assistant_name = db.Column(db.String(255))

    # Relationship
    threads = db.relationship('Thread', backref='assistant')
    messages = db.relationship('Message', backref='assistant')

    def __repr__(self):
        return f'<Assistant {self.assistant_name}>'

class Thread(db.Model):
    __tablename__ = 'threads'
    __table_args__ = {"schema": "chatgpt_schema"}

    thread_id = db.Column(db.String(255), primary_key=True)
    assistant_id = db.Column(db.String(255), db.ForeignKey('chatgpt_schema.assistants.assistant_id'))

    # Relationship
    messages = db.relationship('Message', backref='thread', lazy=True)

    def __repr__(self):
        return f'<Thread {self.thread_id}>'

class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {"schema": "chatgpt_schema"}

    user_message_id = db.Column(db.String(255), primary_key=True)
    bot_message_id = db.Column(db.String(255))
    user_message = db.Column(db.Text)
    bot_message = db.Column(db.Text)
    thread_id = db.Column(db.String(255), db.ForeignKey('chatgpt_schema.threads.thread_id'))
    assistant_id = db.Column(db.String(255), db.ForeignKey('chatgpt_schema.assistants.assistant_id'))

    def __repr__(self):
        return f'<Message {self.message_id}>'