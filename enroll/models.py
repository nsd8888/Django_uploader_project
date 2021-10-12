from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Image(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='myImages/')
    date=models.DateTimeField(auto_now_add=True)
"""
class face_image(models.Model):
    face_access=models.CharField(max_length=500)
    photo=models.ForeignKey(Image, on_delete=models.CASCADE)
    message=models.CharField(max_length=1000,default='hello')
"""
class twitter_image(models.Model):
    API_key=models.CharField(max_length=500)
    API_Secrete_key=models.CharField(max_length=500)
    Access_token=models.CharField(max_length=500)
    Access_token_secrete=models.CharField(max_length=500)
    photo=models.ImageField()
    text=models.TextField(max_length=500)
