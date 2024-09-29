from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from accounts.models import Profile
from base.models import Subject
from .models import AnswerToMessage, Team, Message, FileModelAnswer, FileModelMessage, LookingRival, LookingRivalRequest
from .forms import Create_team_form, Edit_team_form


# Create your views here.

@login_required
def my_teams(request):
    user_teams = Team.objects.filter(members=request.user.profile)
    return render(request, 'teams/my_teams.html', {'teams': user_teams})



@login_required
def create_team(request):
    # if request.method == 'POST':
    #     form = Create_team_form(request.POST)
    #     if form.is_valid():
    #         team = form.save(commit=False)
    #         team.save()
    #         form.save_m2m() 
    #         return redirect('teams/')
    #     else:
    #         print(form.errors)
    # else:
    #     form = Create_team_form()
    # return render(request, 'teams/create_team.html', {'form': form})
    users = Profile.objects.all()
    
    context = {
        'users': users,
    }
    
    if request.method == 'POST':
        # print(f'user {request.POST.getlist('selectUser')}')
        team = Team.objects.create(team_name=request.POST.get('teamName'))
        members = request.POST.getlist('selectUser')
        for member in members:
            team.members.add(member)
        team.save()
        
    return render(request, 'teams/create_team.html', context)


@login_required
def edit_team(request, team_id):
    team = Team.objects.get(id=team_id)
    users = Profile.objects.all()
    
    if request.method == 'POST':
        team.team_name = request.POST.get('teamName')
        team.members.clear()
        members = request.POST.getlist('selectUser')
        for member in members:
            team.members.add(member)
        team.save()
        return redirect('my_teams')
    
    context = {
        'team': team,
        'users': users,
    }
    
    return render(request, 'teams/edit_team.html', context)

def groups(request):
    teams = Team.objects.filter(members=request.user.profile.pk)

    context = {
        'teams': teams,
    }
    return render(request, 'teams/groups.html', context)

def groupChat(request, team_id):
    team = Team.objects.get(pk=team_id)
    
    context = {
        'team': team,
    }

    return render(request, 'teams/group_chat.html', context)

def sendMessage(request, team_id):
    msgId = request.POST['messageId']
    msg = request.POST['msg']
    teamID = request.POST['team_id']
    print(request.FILES.get('file'))

    file = request.FILES.get('file')
    fss = FileSystemStorage()
    filename = fss.save(file.name, file)
    url = fss.url(filename)

    

    if msgId != '':
        answer = AnswerToMessage.objects.create(
            user = request.user.profile,
            message = Message.objects.get(pk=msgId),
            team = Team.objects.get(pk=teamID),
            text = msg,
        )
        FileModelAnswer.objects.create(doc=url, answer=answer)
        return HttpResponse(render(request, 'teams/reply.html', {'answer': answer}))
    else:
        message = Message.objects.create(
            user = request.user.profile,
            team = Team.objects.get(pk=teamID),
            text = msg,
        )
        FileModelMessage.objects.create(doc=url, message=message)
        return HttpResponse(render(request, 'teams/newMessage.html', {'message': message}))
    
import random 

def rivarly(request):
    users = LookingRival.objects.all().exclude(user=request.user.profile)
    sentInvitations = LookingRivalRequest.objects.filter(receiver=request.user.profile)
    yourRivals = LookingRival.objects.filter(user=request.user.profile)

    subjects = Subject.objects.all()

    context = {
        'users': users,    
        'rivarly': sentInvitations,
        'yourRivals': yourRivals,
        'user': request.user.profile,
        'random': random.randint(0, len(subjects)-1),
    }
    return render(request, 'teams/rivarly.html', context)

def invitePeople(request, user_id):
    user = request.user.profile
    userRival = LookingRival.objects.get(user=user)
    
    invitedUserRival = LookingRival.objects.get(user_id=user_id)

    invitation = LookingRivalRequest.objects.create(
        sender = user,
        receiver = invitedUserRival.user,
    )

    return redirect('rivarly')

def acceptPeople(request, sender_id, receiver_id):
    print(sender_id)
    print(receiver_id)

    rival = LookingRivalRequest.objects.get(sender_id=sender_id,
                                    receiver_id=receiver_id)
    
    print(rival)
    rival.accept()

    return redirect('rivarly')