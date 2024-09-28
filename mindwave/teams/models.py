from django.db import models
from accounts.models import Profile

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    # members = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, blank=True, null=True, related_name='team_members')
    members = models.ManyToManyField(Profile, related_name='member_teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def get_messages(self):
        return self.message_set.all() 
        
    def __str__(self):
        return self.team_name
    
class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    time_sent = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        return self.answertomessage_set.all()
    
    def get_files(self):
        return self.filemodelmessage_set.all()

class AnswerToMessage(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    time_sent = models.DateTimeField(auto_now_add=True)

    def get_files(self):
        return self.filemodelanswer_set.all()

class FileModelMessage(models.Model):
    doc = models.FileField(upload_to='media/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

class FileModelAnswer(models.Model):
    doc = models.FileField(upload_to='media/')
    answer = models.ForeignKey(AnswerToMessage, on_delete=models.CASCADE)