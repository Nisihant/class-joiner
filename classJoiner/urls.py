from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='classJoiner'),
    path('getclasses/',views.getclasses,name='getclasses'),
    path('sendMessage/',views.sendMessage,name='sendMessage'),
]