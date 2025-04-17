from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError


class Post(models.Model):
    title = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    content = models.TextField(null=True, blank=True)
    
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