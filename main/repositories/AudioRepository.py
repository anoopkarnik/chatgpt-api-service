from main.models.Audio import Audio
from fuzzywuzzy import fuzz
from extensions import db

class AudioRepository:
    def __init__(self):
        self.model = Audio
    def get_all_audios(self):
        return self.model.query.all()
    def get_audio_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
    def create_audio(self,id,message,location_type,location_path,function_type,voice,model):
        new_audio = self.model(id=id,message=message,location_type=location_type,location_path=location_path,function_type=function_type,voice=voice,model=model)
        db.session.add(new_audio)
        db.session.commit()
        return new_audio
    def update_audio(self,id,message,location_type,location_path,function_type,voice,model):
        audio = self.get_audio_by_id(id)
        audio.message = message
        audio.location_type = location_type
        audio.location_path = location_path
        audio.function_type = function_type
        audio.voice = voice
        audio.model = model
        db.session.add(audio)
        db.session.commit()
        return audio
    def delete_audio(self,id):
        audio = self.get_audio_by_id(id)
        db.session.delete(audio)
        db.session.commit()
        return audio
    def get_audio_by_message(self, message):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.message, message) > 50:
                return audio
        return None
    def get_audio_by_location_path(self, location_path):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.location_path, location_path) > 50:
                return audio
        return None
    def get_audio_by_function_type(self, function_type):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.function_type, function_type) > 50:
                return audio
        return None
    def get_audio_by_voice(self, voice):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.voice, voice) > 50:
                return audio
        return None

    def get_audio_by_location_type(self, location_type):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.location_type, location_type) > 50:
                return audio
        return None
    def get_audio_by_message_and_location_type(self, message, location_type):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.message, message) > 50 and fuzz.ratio(audio.location_type, location_type) > 50:
                return audio
        return None
    def get_audio_by_message_and_location_path(self, message, location_path):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.message, message) > 50 and fuzz.ratio(audio.location_path, location_path) > 50:
                return audio
        return None
    def get_audio_by_message_and_function_type(self, message, function_type):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.message, message) > 50 and fuzz.ratio(audio.function_type, function_type) > 50:
                return audio
        return None
    def get_audio_by_message_and_voice(self, message, voice):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.message, message) > 50 and fuzz.ratio(audio.voice, voice) > 50:
                return audio
        return None

    def get_audio_by_location_type_and_location_path(self, location_type, location_path):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.location_type, location_type) > 50 and fuzz.ratio(audio.location_path, location_path) > 50:
                return audio
        return None
    def get_audio_by_location_type_and_function_type(self, location_type, function_type):
        audios = self.get_all_audios()
        for audio in audios:
            if fuzz.ratio(audio.location_type, location_type) > 50 and fuzz.ratio(audio.function_type, function_type) > 50:
                return audio
        return None

    
