from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_teams, name="my_teams"),
    path('create/', views.create_team, name="create_team"),
    path('edit/<int:team_id>/', views.edit_team, name="edit_team"),
    path('groups/', views.groups, name="groups"),
    path('groups/<str:team_id>/', views.groupChat, name="groupChat"),
    path('groups/<str:team_id>/send-message/', views.sendMessage, name="sendMessage"),
]