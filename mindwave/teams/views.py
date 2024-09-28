from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Team
from .forms import Create_team_form


# Create your views here.

@login_required
def my_teams(request):
    user_teams = Team.objects.filter(members=request.user.profile)
    return render(request, 'teams/my_teams.html', {'teams': user_teams})



@login_required
def create_team(request):
    if request.method == 'POST':
        form = Create_team_form(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.save()
            form.save_m2m() 
            return redirect('teams/')
        else:
            print(form.errors)
    else:
        form = Create_team_form()
    return render(request, 'teams/create_team.html', {'form': form})

@login_required
def edit_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.method == 'POST':
        form = Create_team_form(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('teams/')
    else:
        form = Create_team_form(instance=team)
    return render(request, 'teams/edit_team.html', {'form': form})