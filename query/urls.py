from django.urls import path
from . import views

app_name = 'query'

urlpatterns = [
    path('top', views.top, name='top'),
    path('success', views.success, name='success'),
]