from main.models.Assistant import Thread
from extensions import db


class ThreadRepository:
    def __init__(self):
        self.model = Thread

    def get_all_threads(self):
        return self.model.query.all()

    def get_thread_by_id(self, thread_id):
        return self.model.query.filter_by(thread_id=thread_id).first()

    def create_thread(self, thread_id, assistant_id):
        new_thread = self.model(thread_id=thread_id,assistant_id=assistant_id)
        db.session.add(new_thread)
        db.session.commit()
        return new_thread

    def update_thread(self, thread_id):
        thread = self.get_thread_by_id(thread_id)
        db.session.commit()
        return thread

    def delete_thread(self, thread_id):
        thread = self.get_thread_by_id(thread_id)
        db.session.delete(thread)
        db.session.commit()
        return thread