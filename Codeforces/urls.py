from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
app_name = "Codeforces"

urlpatterns = [
    path('',views.home,name="home"),
    # url(r'^(?P<name>[\w\-\.\@]+)/$', views.analysis, name='analysis'),
]