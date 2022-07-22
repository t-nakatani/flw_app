from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
#from .forms import *
from .models import ImageModel
from .forms import CornerForm
from django.views.generic import CreateView, FormView, TemplateView
from django.conf import settings
from django.contrib import messages

import os, cv2, sys, re, math, Levenshtein, pickle, shutil, math, shutil
import numpy as np
import pandas as pd
import datetime

from infer.infer import *

SIZE_RATIO = 2.5

# Create your views here.
class image_upload(CreateView):
    #テンプレートファイルの連携
    template_name = 'image_upload.html'
    #テーブルの連携
    model = ImageModel
    #入力項目の定義
    fields = ('img', )
    #リダイレクト先を指定
    success_url = reverse_lazy('display_corner')
    # pass

def success(request):
    return render(request,'success.html')

def display_img_lr(request):
    if request.method == 'GET':
        last_img = ImageModel.objects.order_by("id").last() 
        # if not os.path.exists('./data'):
        #     bb, contour4mask, df_n, ARR = infer_arr(str(settings.BASE_DIR) + last_img.img.url)
        shape = result(mode='lr')
        last_img.lr = "img_lr.png" # lr >> left, right
        last_img.save()
        context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
        return render(request, 'display_image_lr.html', context)

    if request.method == 'POST':
        clicked_coord = (request.POST.get('coord_list', None)).split(',')
        if clicked_coord[0] == '': # clickなしにPOSTが起こった場合．#https://office54.net/python/django/display-message-framework
            messages.add_message(request, messages.ERROR, u"ERROR: 修正するラベルを選択してからラベル修正ボタンを押下してください")
            return HttpResponseRedirect(request.path)
        clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
        clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
        last_img = ImageModel.objects.order_by("id").last() 
        update_intersection_label(str(settings.BASE_DIR) + last_img.img.url, clicked_coord)
        shape = result(mode='new_lr')
        # last_img.re_estimate = "img_re_estimate.png"
        context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
        return render(request, 'display_image_re_estimate.html', context)

def display_img_bb(request):
    last_img = ImageModel.objects.order_by("id").last() 
    # last_img.bb = "img_bb.png"
    shape = result(mode='bb')
    context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
    return render(request, 'display_image_bb.html', context)

def display_img_fore(request):
    last_img = ImageModel.objects.order_by("id").last() 
    # last_img.fore = "img_fore.png"
    shape = result(mode='fore')
    context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
    return render(request, 'display_image_fore.html', context)

def display_img_corner(request):
    if request.method == 'GET':
        last_img = ImageModel.objects.order_by("id").last()
        if not os.path.exists('./data'):
            bb, contour4mask, df_n, ARR = infer_arr(str(settings.BASE_DIR) + last_img.img.url)
        shape = result(mode='corner')
        # last_img.corner = "img_corner.png"
        last_img.save()
        context = {
        'first_estimation': True,
        'last_img' : last_img, 
        'height' : shape[0]//SIZE_RATIO, 
        'width' : shape[1]//SIZE_RATIO, 
        }
        return render(request, 'display_image_corner.html', context)
    if request.method == 'POST':
        clicked_coord = (request.POST.get('coord_list', None)).split(',')
        if clicked_coord[0] == '': # clickなしにPOSTが起こった場合．#https://office54.net/python/django/display-message-framework
            messages.add_message(request, messages.ERROR, u"ERROR: 花弁の重なり位置を選択してから再推定ボタンを押下してください")
            return HttpResponseRedirect(request.path)
        clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
        clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
        last_img = ImageModel.objects.order_by("id").last() 
        # img_path = str(settings.BASE_DIR) + last_img.img.url
        re_infer_with_clicked('./data/img.png', clicked_coord)
        shape = result(mode='new_corner')
        # last_img.re_estimate = "img_corner_2nd.png"
        context = {
            'first_estimation': False,
            'last_img' : last_img, 
            'height' : shape[0]//SIZE_RATIO, 
            'width' : shape[1]//SIZE_RATIO
            }
        return render(request, 'display_image_corner.html', context)
        # https://docs.djangoproject.com/ja/4.0/ref/urlresolvers/#django.urls.reverse
        # return HttpResponseRedirect(reverse('display_lr'))
        


def home(request):
    if os.path.exists('./data'):
        dt = get_date_str()
        dst = f'./log_result/{dt}/'
        os.mkdir(dst)
        try:
            shutil.move('./data/img.png', dst)
            shutil.move('./data/log_result.json', dst)
            shutil.move('./data/df_n.csv', dst)
        except:
            print('there isnt enough result data !!')
        shutil.rmtree('./data')

    return render(request, 'home.html')

def result(mode):
    path = str(settings.BASE_DIR) + f'/data/img_{mode}.png'
    img = cv2.imread(path)
    result_img = img
    output = str(settings.BASE_DIR) + f"/media/img_{mode}.png"
    cv2.imwrite(output, result_img)

    return img.shape

def get_date_str():
        t_delta = datetime.timedelta(hours=9)  # 9時間
        JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
        dt = datetime.datetime.now(JST)  # タイムゾーン付きでローカルな日付と時刻を取得
        dt = str(dt).split('.')[0].replace(' ', '-').replace(':', '')
        return dt
    

   