from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if img.height > 400 or img.width > 400:
                output_size = (400,400)
                img.thumbnail(output_size)
                img.save(self.image.path)
                
        except UnidentifiedImageError:
            print(f"Could not identify image at {self.image.path}")