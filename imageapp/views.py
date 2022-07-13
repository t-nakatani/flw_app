from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
#from .forms import *
from .models import ImageModel
from django.views.generic import CreateView
from django.conf import settings

import os, cv2, sys, re, math, Levenshtein, pickle, shutil, math, shutil
import numpy as np
import pandas as pd

from infer.infer import *

# Create your views here.
class image_upload(CreateView):
    if os.path.exists('data'):
        shutil.rmtree('data')
    #テンプレートファイルの連携
    template_name = 'image_upload.html'
    #テーブルの連携
    model = ImageModel
    #入力項目の定義
    fields = ('name', 'author', 'img')
    #リダイレクト先を指定
    success_url = reverse_lazy('display_lr')
    pass

def success(request):
    return render(request,'success.html')

def display_img_lr(request):
    SIZE_RATIO = 2.5
    if request.method == 'GET':
        last_img = ImageModel.objects.order_by("id").last() 

        if not os.path.exists('data'):
            bb, contour4mask, df_n, ARR = infer_arr(str(settings.BASE_DIR) + last_img.img.url)
        shape = result(mode='lr')
        last_img.lr = "img_lr.png" # lr >> left, right
        last_img.save()
        context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
        return render(request, 'display_image_lr.html', context)

    if request.method == 'POST':
        clicked_coord = (request.POST.get('coord_list', None)).split(',')
        clicked_coord = list(map(int, clicked_coord))
        clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
        last_img = ImageModel.objects.order_by("id").last() 
        update_intersection_label(str(settings.BASE_DIR) + last_img.img.url, clicked_coord, SIZE_RATIO)
        shape = result(mode='re_estimate')
        last_img.re_estimate = "img_re_estimate.png"
        context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
        return render(request, 'display_image_re_estimate.html', context)

def display_img_bb(request):
    last_img = ImageModel.objects.order_by("id").last() 
    last_img.bb = "img_bb.png"
    shape = result(mode='bb')
    context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
    return render(request, 'display_image_bb.html', context)

def display_img_fore(request):
    last_img = ImageModel.objects.order_by("id").last() 
    last_img.fore = "img_fore.png"
    shape = result(mode='fore')
    context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
    return render(request, 'display_image_fore.html', context)

def home(request):
    return render(request, 'home.html')

def result(mode):
    path = str(settings.BASE_DIR) + f'/data/img_{mode}.png'
    img = cv2.imread(path)
    result_img = img
    output = str(settings.BASE_DIR) + f"/media/img_{mode}.png"
    cv2.imwrite(output, result_img)

    return img.shape

   