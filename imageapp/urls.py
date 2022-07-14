from django.urls import path
# from .views import image_upload, success, display_img_lr, display_img_bb, display_img_fore, home
from .views import *

urlpatterns = [
    path('image_upload/', image_upload.as_view(), name='upload'),
    path('success/', success, name='success'),
    path('display_image_lr', display_img_lr, name='display_lr'),
    path('display_image_corner', display_img_corner, name='display_corner'),
    path('display_image_re_estimate', display_img_lr, name='display_re_estimate'),
    path('display_image_bb',display_img_bb, name='display_bb'),
    path('display_image_fore',display_img_fore, name='display_fore'),
    path('home', home, name='home'),
    # path("display_corner", display_corner.as_view(), name='display_img_corner'),
]