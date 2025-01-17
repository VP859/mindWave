from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('quizes/', views.quizes, name="quizes"),
    path('quizes/<str:pk>/', views.quiz, name="quiz"),
    path('quizes/<str:pk>/<str:sender>/<str:receiver>/', views.quiz, name="quiz"),
    path('add-score/', views.addScore, name="addScore"),


    path('add-score/<str:sender>/<str:receiver>/', views.addScore, name="addScore"),
    path('ranking/', views.ranking, name="ranking"),
]