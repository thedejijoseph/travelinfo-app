
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('terminals/new', views.terminals_new),
]
