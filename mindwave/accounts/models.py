from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
import os

# Create your models here.
def get_upload_path(instance, filename):
    upload_to = 'profile_pictures/'
    
    ext = filename.split('.')[-1]

    filepath = os.path.join(upload_to, ext)

    if os.path.exists(os.path.join('media', filepath)):
        filename = f'{filename.split(".")[0]}.{ext}'

    
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    ranks = (
            ('IRON', 'IRON'),
            ('BRONZE', 'BRONZE'),
            ('SILVER', 'SILVER'),
            ('GOLD', 'GOLD'),
            ('PLATINUM', 'PLATINUM'),
            ('EMERALD', 'EMERALD'),
            ('DIAMOND', 'DIAMOND'),
            )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField(default=25)
    profile_picture = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    teams = models.ForeignKey('teams.Team', on_delete=models.CASCADE, blank=True, null=True)
    
    roles = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = models.CharField(max_length=10, choices=roles, default='student')
    
    points = models.IntegerField(default=0)
    rank = models.CharField(choices=ranks, max_length=30, default='IRON')

    def __str__(self):
        return self.user.username
        
