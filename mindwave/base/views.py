from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from accounts.models import Profile
from .models import Subject, Quiz, Score, FunFact

import random
import os
import google.generativeai as genai

from teams.models import RivalScore


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        random.seed()
        try:
            random_index = random.randint(0, FunFact.objects.count() - 1)
        except:
            random_index = 0

        try:
            fact = FunFact.objects.all()[random_index]
            print(fact)
        
            text = fact.fact
            category = fact.category
            
            fun_facts = []
            
            fun_facts.append([text, category])
            
            print(fun_facts)
            
        
        except:
            fun_facts = []
        response = generate('You are a teacher and you want to advise student on how to improve their learning skills and habits. What would you say? only plain text up to 200 chars')
        return render(request, 'homeForLogged.html', {'fun_facts': fun_facts, 'advise': 'response', 'user': request.user}) 
    else:
        return render(request, 'homeForLogged.html')

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



def generate(prompt):
    genai.configure(api_key=os.environ["API_KEY"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(prompt)
    
    temp = response.text
    
    formatted_response = mark_safe(temp.replace("**", " <b> <br>").replace("***", " <i> <br>").replace("****", " <u> <br>"))

    return formatted_response
