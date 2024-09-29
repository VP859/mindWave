from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Subject),
admin.site.register(Quiz),
admin.site.register(Question),
admin.site.register(Answer),
admin.site.register(Score),
admin.site.register(DiagnosticTest),
admin.site.register(DiagnosticCategory),
admin.site.register(DiagnosticQuestion),
admin.site.register(DiagnosticAnswer),
admin.site.register(DiagnosticScore),
admin.site.register(FunFact),