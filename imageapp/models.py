from django.db import models

# Create your models here.

class ImageModel(models.Model):
    # name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='')
    # author = models.CharField(max_length=100, null=True)
    
    #アップロードされた画像を処理したもの
    lr = models.ImageField(default='img_lr.png')
    corner = models.ImageField(default='img_corner.png')
    bb = models.ImageField(default='img_bb.png')
    fore = models.ImageField(default='img_fore.png')
    new_corner = models.ImageField(default='img_new_corner.png')
    new_lr = models.ImageField(default='img_new_lr.png')