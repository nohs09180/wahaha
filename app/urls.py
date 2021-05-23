from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.top, name=''),
    path('camera_session/', views.camera_session, name='camera_session'),
    path('camera/', views.camera, name='camera'),
    path('video_list/', views.video_list, name='video_list'),
    path('video_list/<int:video_id>/', views.video_detail, name='video_detail'),
    path('mypage/', views.mypage, name='mypage'),
    path('get_data/', views.get_data, name='get_data'),
]