from django.db import models

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    members = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, blank=True, null=True, related_name='team_members')
    created_at = models.DateTimeField(auto_now_add=True)   
    
    
    def __str__(self):
        return self.team_name