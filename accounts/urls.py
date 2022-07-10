from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='accounts'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('verifyToken/<username>', views.verifyToken, name='verifyToken'),
    path('success/', views.success, name='success'),
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('VerifyForgetToken/<username>/<auth_token>', views.VerifyForgetToken, name='VerifyForgetToken'),
    path('logout', views.logout, name='logout'),
    path('fetchUserLastCode', views.fetchUserLastCode, name='fetchUserLastCode'),
    path('getLastSettings', views.getLastSettings, name='getLastSettings'),
    path('myCodes', views.myCodes, name='myCodes'),
]
