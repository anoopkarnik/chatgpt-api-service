from main.models.Image import Image
from fuzzywuzzy import fuzz
from extensions import db

class ImageRepository:
    def __init__(self):
        self.model = Image
    def get_all_images(self):
        return self.model.query.all()
    def get_image_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
    def create_image(self,id,prompt,revised_prompt,location_type,location_path,function_type,image_size,model,
                     quality,variations,style):
        new_image = self.model(id=id,prompt=prompt,revised_prompt=revised_prompt,location_type=location_type,
                               location_path=location_path,function_type=function_type,image_size=image_size,
                               model=model,quality=quality,variations=variations,style=style)
        db.session.add(new_image)
        db.session.commit()
        return new_image
    def update_image(self,id,prompt,revised_prompt,location_type,location_path,function_type,image_size,model,quality,variations,style):
        image = self.get_image_by_id(id)
        image.prompt = prompt
        image.revised_prompt = revised_prompt
        image.location_type = location_type
        image.location_path = location_path
        image.function_type = function_type
        image.image_size = image_size
        image.model = model
        image.quality = quality
        image.variations = variations
        image.style = style
        db.session.add(image)
        db.session.commit()
        return image
    def delete_image(self,id):
        image = self.get_image_by_id(id)
        db.session.delete(image)
        db.session.commit()
        return image
    def get_image_by_prompt(self, prompt):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.prompt, prompt) > 50:
                return image
        return None
    def get_image_by_revised_prompt(self, revised_prompt):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.revised_prompt, revised_prompt) > 50:
                return image
        return None
    def get_image_by_location_path(self, location_path):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.location_path, location_path) > 50:
                return image
        return None
    def get_image_by_function_type(self, function_type):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.function_type, function_type) > 50:
                return image
        return None
    def get_image_by_image_size(self, image_size):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.image_size, image_size) > 50:
                return image
        return None
    def get_image_by_model(self, model):
        images = self.get_all_images()
        for image in images:
            if fuzz.ratio(image.model, model) > 50:
                return image
        return None