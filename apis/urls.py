from django.contrib import admin
from django.urls import path
from django.conf import settings
from apis import views

urlpatterns = [
    path('AllMlProjects/', views.AllMlProjects, name='AllMlProjects'),
    path('AllToolBox/', views.AllToolBox, name='AllToolBox'),
]
