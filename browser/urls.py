
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('terminals/new', views.terminals_new),
    path('terminals/<uuid:terminal_id>/edit', views.terminals_edit),
    path('terminals/<uuid:terminal_id>', views.terminals_page),
    path('terminals', views.terminals_all),
    path('states/<str:state_id>', views.states_page),
    path('states', views.states_all),
    path('about', views.about_page),
    path('chatbot', views.chatbot_page),
]
