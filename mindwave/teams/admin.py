from django.contrib import admin
from .models import Team, Message, AnswerToMessage, FileModelAnswer, FileModelMessage

# Register your models here.
admin.site.register(Team)
admin.site.register(Message)
admin.site.register(AnswerToMessage)
admin.site.register(FileModelAnswer)
admin.site.register(FileModelMessage)