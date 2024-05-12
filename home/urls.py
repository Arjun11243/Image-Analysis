from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index,name='home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('upload', views.upload, name='upload'),
    path('doc_verify', views.doc_verify, name='doc_verify'),
    path('authentication', views.authentication, name='authentication'),
]