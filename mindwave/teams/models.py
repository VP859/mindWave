from django.db import models
from accounts.models import Profile

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    # members = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, blank=True, null=True, related_name='team_members')
    members = models.ManyToManyField(Profile, related_name='member_teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def save(self, *args, **kwargs):
        print(f'args: {args[0]}')
        for manager in args[0]:
            print(f'manager: {manager}')
        super(Team, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.team_name