from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import get_user_model
from .models import Video, SmileData, SmileRate, SmileDosData, SmileDos
import sys
sys.path.append('../')
from users.models import User
from django.http.response import JsonResponse
import json 
from django.utils import timezone

from io import StringIO, BytesIO
from PIL import Image
import sys
import time
import numpy as np
import cv2
import webbrowser
import csv
import re
import base64

# import cognitive_face as CF
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

User = get_user_model()

def top(request):
    return render(request, 'app/top.html')

def camera_session(request):
    return render(request, 'app/camera_session.html')

def camera(request):
    return render(request, 'app/camera.html')

def video_list(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'app/video_list.html', context)

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    context = {'v': video}
    return render(request, 'app/video_detail.html', context)

def mypage(request):
    user = request.user
    context = {'user': user}
    return render(request, 'app/mypage.html', context)


def smile_detection(image):
    # print(image)
    smile = 0

    face_cascade = cv2.CascadeClassifier('app/haarcascades/haarcascade_frontalface_default.xml') 
    smile_cascade = cv2.CascadeClassifier('app/haarcascades/haarcascade_smile.xml')
    
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 130, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_img = img[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.11, minNeighbors=100, minSize = (80, 40))
        if len(smiles) > 0 : 
            smile = 1
        else:
            smile = 0
        # for (x_smile, y_smile, w_smile, h_smile) in smiles: 
        #     cv2.rectangle(img,(x+x_smile, y+y_smile),(x+x_smile+w_smile, y+y_smile+h_smile), (255, 0, 130), 2)
    # cv2.imwrite('app/face_smile.png', img)
    return smile

def get_data(request):
    img_decode = request.POST.get('image')
    # print('img_decode', len(img_decode.split(':')[1]))
    if len(img_decode.split(':')[1]) == 1:
        print('no image')
        return HttpResponse()
    else:
        img_byte = base64.b64decode(img_decode.split(',')[1])
        img_byte = BytesIO(img_byte)
        img_rgba = Image.open(img_byte)
        img_rgb = img_rgba.convert('RGB')
        img_before = cv2.imread('app/face.png')
        img_rgb.save('app/face.png')
        img = 'app/face.png'
        img_after = cv2.imread(img)
        if np.array_equal(img_before, img_after):
            print('image is no change')
            return HttpResponse()
        else:
            smile = smile_detection(img)
            s = SmileData(person=User.objects.get(email='java@java.com'), video=Video.objects.get(name='ex4'), data=smile, data_joined=timezone.now())
            s.save()
            print('get_data', smile)
            return HttpResponse(smile)



def Euclid_dis(data1, data2):
    if len(data1) > len(data2):
        del data1[len(data2):]
    elif len(data2) > len(data1):
        del data2[len(data1):]
    
    squared_sum = 0

    for i in range(len(data1)):
        squared = (data1[i] - data2[i]) ** 2
        squared_sum += squared

    return np.sqrt(squared_sum)

def calc_smile_rate(request, video_id):
    data = SmileData.objects.filter(
        person=User.objects.get(email=request.user),
        video=Video.objects.get(id=video_id)
    )
    data_list = list(map(int, data.values_list('data', flat=True)))
    smile_rate = np.nansum(data_list) / (len(data_list) - np.count_nonzero(np.isnan(data_list))) * 100
    s = SmileRate(user=request.user, 
        video=Video.objects.get(id=video_id).name, 
        smile_rate=round(smile_rate, 1), 
        joined=timezone.now())
    s.save()
    return HttpResponse()

def calc_smile_dos(request, video_id):
    user_list = SmileRate.objects.filter(video=Video.objects.get(id=video_id).name)
    user_list = list(user_list.values_list('user', flat=True))

    if request.user in user_list:
        data_df = pd.Series([], dtype='float32')
        for user in user_list:
            data = SmileData.objects.filter(
                person=User.objects.get(email=user), 
                video=Video.objects.get(id=video_id)
            )
            data_list = list(map(int, data.values_list('data', flat=True)))
            data_se = pd.Series(data_list, name=user)
            data_df = pd.concat([data_df, data_se], axis=1)

        dos_dict = {}
        user_list.remove(request.user)
        user1 = data_df[request.user].values.tolist()
        for user in user_list:
            user2 = data_df[user].values.tolist()
            dos = 1 / (1 + Euclid_dis(user1, user2)) * 100
            s = SmileDos(
                user1=request.user,
                user2=user,
                video=Video.objects.get(id=video_id),
                smile_dos=round(dos, 1),
                joined=timezone.now()
            )
            s.save()
        return HttpResponse()
    else:
        print('ログインユーザーが含まれていません')
        return HttpResponse()

def calc_smile_dos_mean(request, video_id):
    user_list1 = SmileDosData.objects.filter(user1=request.user)
    user_list1 = list(user_list1.values_list('user2', flat=True))
    user_list2 = SmileDosData.objects.filter(user2=request.user)
    user_list2 = list(user_list2.values_list('user1', flat=True))
    user_list = list(set(user_list1 + user_list2))

    for user in user_list:
        smile_dos1 = SmileDosData.objects.filter(user1=request.user, user2=user)
        smile_dos1 = list(map(int, smile_dos1.values_list('smile_dos', flat=True)))
        smile_dos2 = SmileDosData.objects.filter(user1=user, user2=request.user)
        smile_dos2 = list(map(int, smile_dos2.values_list('smile_dos', flat=True)))
        smile_dos_mean = np.mean(smile_dos1 + smile_dos2)
        s = smile_dos(
            user1=request.user,
            user2=user,
            smile_dos=round(smile_dos_mean, 1),
            joined=timezone.now()
        )
        s.save()
    return HttpResponse()


        
# def calc_recommand(request, video_id):
#     user = 
#     for user in user_list:
#         video_list = UserVideoSet.objects.filter(user=user)
#         video_list = video_list.values_list('video', flat=True)
#         video_list = list(video_list)

#     calc_dict = {}
#     for name in name_list:
#         calc_dict[(name, df_rate[name].idxmax())] = df_DoS[name]['ave'] * df_rate[name].max()
#     s_calc = pd.Series(calc_dict)
#     recommend_video = s_calc.idxmax()[1]


#レコメンド動画の決定(類似度×笑顔率)
# calc_dict = {}
# for name in name_list:
#     calc_dict[(name, df_rate[name].idxmax())] = df_DoS[name]['ave'] * df_rate[name].max()
# s_calc = pd.Series(calc_dict)
# recommend_video = s_calc.idxmax()[1]
#     user = User.objects.get(email=request.user)
#     user_id = user.id

#     data = SmileData.objects.filter(
#         person=User.objects.get(email=), 
#         video=Video.objects.get(id=ex1)
#     )
#     data = data.values_list('data', flat=True)
#     data = list(map(int, data))


    




#sessionで使用
# def mk_session(request):
#     request.session['video'] = {}
#     # request.session['video'].append(1)
#     print('mk_session', request.session['video'])
#     return HttpResponse()

# def storage_session(request):
#     s = SmileData(person=User.objects.get(id=1), video=Video.objects.get(id=1))
#     s.save()
#     return HttpResponse()

# def print_session(request):
#     print('print_session', request.session['video'])
#     # return redirect('app:camera')
#     return render(request, 'app/camera.html')

# def append_session(request):
#     request.session['video'][1] = 1
#     print(request.session['video'])
#     return HttpResponse(request.session['video'])    
    


# PILでRGBを変更するコード
# r, g, b, a = img.split()
# img = Image.merge('RGBA', (r, g, b, a))
# img2 = Image.merge('RGBA', (r, b, g, a))


#別解　ただしうまくいってない
# json_str = request.body.decode("utf-8") 　# json_strの値は<image=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAA>
# json_data = json.loads(json_str)
# img_binary = base64.b64decode(json_str[37:])
# img = np.frombuffer(img_binary, dtype=np.uint8)
# img = cv2.imdecode(img, cv2.IMREAD_COLOR)
# img = np.array(img, 'uint8')

