from django.shortcuts import render
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.conf import settings
from . import forms
import json

# basic response view
@login_required
def get_response(request):
    api_key = settings.API_KEY
    
    if not api_key:
        raise ValueError("API_KEY not set")
    
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-s    ettings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    # take prompt from user
    if request.method == "POST":
        form = forms.GPTRequestForm(request.POST)
        if form.is_valid():
            prompt = f'{form.cleaned_data["prompt"]} for user at age {request.user.profile.age}'
            response = chat_session.send_message(prompt)
            response = response.text
            formatted_response = mark_safe(response.replace("**", " <b> <br>").replace("***", " <i> <br>").replace("****", " <u> <br>"))
            return render(request, "gpt/response.html", {"response": formatted_response})
    else:
        form = forms.GPTRequestForm()
    
    response = chat_session.send_message("Hello")
    

    return render(request, "gpt/response.html", {"response": response.text, "form": form})


@login_required
def ai_quiz(request):
    api_key = settings.API_KEY
    
    if not api_key:
        raise ValueError("API_KEY not set")
    
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    'top_k': 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-s    ettings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    # take prompt from user
    if request.method == "POST":
        form = forms.GPTQuizForm(request.POST)
        if form.is_valid():
            mixed_answers_count = form.cleaned_data.get("mixed_answers_count")
            if mixed_answers_count:
                prompt = f'make quiz in category {form.cleaned_data["category"]} that have {form.cleaned_data["questions_count"]} questions with 2 to 5 answers'
                
            prompt = f'make quiz in category {form.cleaned_data["category"]} that have {form.cleaned_data["questions_count"]} questions with {form.cleaned_data["answers_count"]} answers'
            response = chat_session.send_message(prompt)
            response = response.text
            
            formatted_response = format_json_response(response)
           
            
            return render(request, "gpt/ai_quiz.html", {"response": formatted_response, 'form': form})
    else:
        form = forms.GPTQuizForm()
    
    response = chat_session.send_message("Hello")
    
    return render(request, "gpt/ai_quiz.html", {"response": response.text, "form": form})

# format json response

def format_json_response(response):
    try:
        response_dict = json.loads(response)
        formatted_questions = []

        for question in response_dict.get("questions", []):
            formatted_question = {
                "question": question.get("question"),
                "answers": question.get("answers"),
                "correct_answer": question.get("correct_answer")
            }
            formatted_questions.append(formatted_question)

        print(formatted_questions[0])
        
        return formatted_questions
    except json.JSONDecodeError:
        return "Invalid JSON response"