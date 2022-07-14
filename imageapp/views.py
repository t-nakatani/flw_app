from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
#from .forms import *
from .models import ImageModel
from .forms import CornerForm
from django.views.generic import CreateView, FormView, TemplateView
from django.conf import settings

import os, cv2, sys, re, math, Levenshtein, pickle, shutil, math, shutil
import numpy as np
import pandas as pd

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
    success_url = reverse_lazy('display_lr')
    # pass

def success(request):
    return render(request,'success.html')

def display_img_lr(request):
    if request.method == 'GET':
        last_img = ImageModel.objects.order_by("id").last() 
        if not os.path.exists('./data'):
            bb, contour4mask, df_n, ARR = infer_arr(str(settings.BASE_DIR) + last_img.img.url)
        shape = result(mode='lr')
        last_img.lr = "img_lr.png" # lr >> left, right
        last_img.save()
        context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
        return render(request, 'display_image_lr.html', context)

    if request.method == 'POST':
        clicked_coord = (request.POST.get('coord_list', None)).split(',')
        clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
        clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
        last_img = ImageModel.objects.order_by("id").last() 
        update_intersection_label(str(settings.BASE_DIR) + last_img.img.url, clicked_coord)
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

def display_img_corner(request):
    if request.method == 'GET':
        last_img = ImageModel.objects.order_by("id").last() 
        # last_img.xxx = "img_xxx.png"
        shape = result(mode='lr')
        last_img.lr = "img_lr.png"
        last_img.save()
        context = {
        'last_img' : last_img, 
        'height' : shape[0]//SIZE_RATIO, 
        'width' : shape[1]//SIZE_RATIO, 
        # 'updated' : True
        }
        return render(request, 'display_image_corner.html', context)
    if request.method == 'POST':
        clicked_coord = (request.POST.get('coord_list', None)).split(',')
        clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
        clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
        last_img = ImageModel.objects.order_by("id").last() 
        img_path = str(settings.BASE_DIR) + last_img.img.url
        re_infer_with_clicked('./data/img.png', clicked_coord)
        shape = result(mode='lr')
        last_img.re_estimate = "img_lr.png"
        context = {
        'last_img' : last_img, 
        'height' : shape[0]//SIZE_RATIO, 
        'width' : shape[1]//SIZE_RATIO, 
        # 'updated' : False
        }
        # https://docs.djangoproject.com/ja/4.0/ref/urlresolvers/#django.urls.reverse
        return HttpResponseRedirect(reverse('display_lr'))
        


def home(request):
    if os.path.exists('./data'):
        shutil.rmtree('./data')
    return render(request, 'home.html')

def result(mode):
    path = str(settings.BASE_DIR) + f'/data/img_{mode}.png'
    img = cv2.imread(path)
    result_img = img
    output = str(settings.BASE_DIR) + f"/media/img_{mode}.png"
    cv2.imwrite(output, result_img)

    return img.shape


# class display_corner(TemplateView):
#     template_name = 'display_image_corner.html'
#     success_url = 'display_image_lr'
#     def get_success_url(self):
#         return reverse_lazy('report_detail', kwargs={'pk': self.object.id})

#     def get(self, request, *args, **kwargs):
#         last_img = ImageModel.objects.order_by("id").last() 
#         # last_img.xxx = "img_xxx.png"
#         shape = result(mode='lr')
#         last_img.lr = "img_lr.png"
#         last_img.save()
#         context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
#         # return self.render_to_response(self.get_context_data(context))
#         return self.render_to_response(context)

#     def post(self, request, *args, **kwargs):
#         clicked_coord = (request.POST.get('coord_list', None)).split(',')
#         clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
#         clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
#         last_img = ImageModel.objects.order_by("id").last() 
#         img_path = str(settings.BASE_DIR) + last_img.img.url
#         re_infer_with_clicked('./data/img.png', clicked_coord)
#         shape = result(mode='lr')
#         last_img.re_estimate = "img_lr.png"
#         context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
#         return render(request, 'display_image_lr.html', context)

# class display_corner(FormView):
#     template_name = 'display_image_lr.html'
#     form_class = CornerForm
#     success_url = 'display_image_lr'


#     # get()のオーバーライド
#     def get(self, request, *args, **kwargs):
#         self.template_name = 'display_image_corner.html'
#         last_img = ImageModel.objects.order_by("id").last() 
#         # last_img.xxx = "img_xxx.png"
#         shape = result(mode='lr')
#         last_img.lr = "img_lr.png"
#         last_img.save()
#         context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
#         # return self.render_to_response(self.get_context_data(context))
#         return self.render_to_response(context)


#     # form_valid()のオーバーライド
#     def form_valid(self, form):
#         print('==========', form.cleaned_data.keys())
#         # print('==========', form.instance)
#         # print(form.instance)
#         clicked_coord = form.cleaned_data['coord_list'].split(',')
#         clicked_coord = list(map(lambda x: int(int(x)*SIZE_RATIO), clicked_coord))
#         clicked_coord = np.array(clicked_coord).reshape(-1, 2)
        
#         last_img = ImageModel.objects.order_by("id").last() 
#         img_path = str(settings.BASE_DIR) + last_img.img.url
#         re_infer_with_clicked('./data/img.png', clicked_coord)
#         shape = result(mode='lr')
#         last_img.re_estimate = "img_lr.png"
#         context = {'last_img' : last_img, 'height' : shape[0]//SIZE_RATIO, 'width' : shape[1]//SIZE_RATIO}
#         return render(request, 'display_image_lr.html', context)
    




















   