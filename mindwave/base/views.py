from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Profile
from .models import Subject, Quiz, Score
from teams.models import RivalScore


# Create your views here.
def home(request):
    if request.user:
        return render(request, 'homeForLogged.html')
    else:
        pass

def quizes(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects,
    }
    return render(request, 'quiz/quizes.html', context)

def quiz(request, pk, sender=None, receiver=None):
    quiz = Quiz.objects.get(pk=pk)
    print(sender)
    print(receiver)

    context = {
        'quiz': quiz,
        'sender': sender,
        'receiver': receiver,
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

    # if sender and receiver:
    #     try:
    #         RivalScore.objects.create(
    #             quiz=quiz,
    #             sender_id=sender,
    #             receiver_id=receiver,
    #             senderScore=score,
    #             receiverScore=score,
    #         )
    #     except:
    #         rscore = RivalScore.objects.get(
    #             quiz=quiz,
    #             sender_id=sender,
    #             receiver_id=receiver,
    #         )

    #         if rscore.senderScore:
    #             rscore.receiverScore = score
    #         else:
    #             rscore.senderScore = score

    #         rscore.save()

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