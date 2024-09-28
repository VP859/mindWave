from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Profile
from .models import Subject, Quiz, Score


# Create your views here.
def home(request):
    return render(request, 'base.html')

def quizes(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects,
    }
    return render(request, 'quiz/quizes.html', context)

def quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)

    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz/quiz.html', context)

def addScore(request):
    quiz = request.POST['quiz']
    score = request.POST['score']

    print(quiz)
    print(score)

    quiz = Quiz.objects.get(pk=quiz)
    print(quiz)
    
    try:
        scoreObj = Score.objects.get(quiz=quiz)
        request.user.profile.points -= scoreObj.points
        request.user.profile.points += int(score)
        scoreObj.points = int(score)
        scoreObj.save()
    except:
        Score.objects.create(user=request.user.profile, quiz=quiz, points=score)
        request.user.profile.points += int(score)

    return JsonResponse({})

def ranking(request):
    users = Profile.objects.all().order_by('-points')[0:10]
    ranks = reversed(list(Profile.ranks))

    context = {
        'user': request.user.profile,
        'ranks': {},
    }

    for rank in ranks:
        context['ranks'].update({
            rank[0]: Profile.objects.filter(rank=rank[0]).order_by('-points'),
        })

    subjects = Subject.objects.all()

    context['quizes'] = {}

    for subject in subjects:
        context['quizes'].update({
            subject: {}
        })

        for quiz in subject.get_quizes():
            for score in quiz.get_scores():
                context['quizes'][subject].update({
                    score.user.user.username: score.points,
                })

    return render(request, 'quiz/ranking.html', context)