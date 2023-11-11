from main.models.Assistant import Assistant
from extensions import db


class AssistantRepository:
    def __init__(self):
        self.model = Assistant

    def get_all_assistants(self):
        return self.model.query.all()
    
    def get_assistant_by_id(self, assistant_id):
        return self.model.query.filter_by(assistant_id=assistant_id).first()
    
    def get_assistant_by_name(self, assistant_name):
        return self.model.query.filter_by(assistant_name=assistant_name).first()

    def create_assistant(self, assistant_id, assistant_name):
        new_assistant = self.model(assistant_id=assistant_id,assistant_name=assistant_name)
        db.session.add(new_assistant)
        db.session.commit()
        return new_assistant
    
    def update_assistant(self, assistant_id, assistant_name):
        assistant = self.get_assistant_by_id(assistant_id)
        assistant.assistant_name = assistant_name
        db.session.commit()
        return assistant
    
    def delete_assistant(self, assistant_id):
        assistant = self.get_assistant_by_id(assistant_id)
        db.session.delete(assistant)
        db.session.commit()
        return assistant
