from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_response, name="get_response"),
    path('quiz/', views.ai_quiz, name="ai_quiz"),
]
