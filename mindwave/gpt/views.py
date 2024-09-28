from django.shortcuts import render
from dotenv import load_dotenv
import os
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import forms


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
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    # take prompt from user
    if request.method == "POST":
        form = forms.GPTRequestForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            response = chat_session.send_message(prompt)
            response = response.text
            return render(request, "gpt/response.html", {"response": response})
    else:
        form = forms.GPTRequestForm()
    
    response = chat_session.send_message("Hello")
    

    return render(request, "gpt/response.html", {"response": response.text, "form": form})
