from django.db import models

# Create your models here.

class ImageModel(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='')
    author = models.CharField(max_length=100, null=True)
    #アップロードされた画像を処理したもの
    gray = models.ImageField(default='Not Set')