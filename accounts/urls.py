from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('statistics/', views.statistics, name='statistics'),
    path('medical-records/', views.medicalRecords, name='records'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addrecord/', views.addrecord, name='addrecord'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
]