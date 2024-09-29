from django.contrib import admin
from .models import Team, Message, AnswerToMessage, FileModelAnswer, FileModelMessage, LookingRival, LookingRivalRequest

# Register your models here.
admin.site.register(Team)
admin.site.register(Message)
admin.site.register(AnswerToMessage)
admin.site.register(FileModelAnswer)
admin.site.register(FileModelMessage)
admin.site.register(LookingRival)
admin.site.register(LookingRivalRequest)