from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import User

from .models import InterviewAnswer
from django.contrib import messages
from django.shortcuts import redirect


import librosa
import numpy as np
import joblib

import re
import json

import soundfile as sf
import sounddevice as sd
import os
from django.conf import settings


def home(request):
    return render(request, "home.html")

@login_required
def start(request):
    return render(request, "start.html")

@login_required
def voice(request):
    return render(request, "voice.html")



import wandb
import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display, Markdown

# For formatting
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# gemini_api_key = input ("What is your Gemini API key? :") 
genai.configure(api_key='AIzaSyCIss-VVb5Rxk0j3Z3rOmRzB5lTzD3b6sY')
# print(gemini_api_key) 

model = genai.GenerativeModel('gemini-pro')

def chat(request):
    questions = ""
    labels = ""
    Question1 = ""
    Question2 = ""
    Question3 = ""
    Question4 = ""
    # if request.method == "POST":
    i = 1
    questions = ""
    
    response = model.generate_content(''' give me one question in computer ? ''')
    Question1 = to_markdown(response.text)
    print(Question1)
    response = model.generate_content(''' give me one question in computer ? ''')
    Question2 = to_markdown(response.text)
    print()
    response = model.generate_content(''' give me one question in computer ? ''')
    Question3 = to_markdown(response.text)
    print(Question3)
    response = model.generate_content(''' give me one question in computer ? ''')
    Question4 = to_markdown(response.text)
    print(Question4)


    if Question1:
        print("Question 1:", Question1)
    if Question2:
        print("Question 2:", Question2)
    if Question3:
        print("Question 3:", Question3)
    if Question4:
        print("Question 4:", Question4)
    
    questions = Question1 + Question2 + Question3 + Question4

    context ={
        'questions': questions,
        'Question1': Question1 if Question1 else None,
        'Question2': Question2 if Question2 else None,
        'Question3': Question3 if Question3 else None,
        'Question4': Question4 if Question4 else None,
    }
    return render(request, "chat.html", context)



def evaluate(request):
    rate1 = ''
    rate2 = ''
    rate3 = ''
    rate4 = ''
    label1 = ''
    label2 = ''
    label3 = ''
    label4 = ''
    
    if request.method == "POST":
        Answer1 = request.POST.get("Question1", "")
        label1 = request.POST.get("label1", "")
        Answer2 = request.POST.get("Question2", "")
        label2 = request.POST.get("label2", "")
        Answer3 = request.POST.get("Question3", "")
        label3 = request.POST.get("label3", "")
        Answer4 = request.POST.get("Question4", "")
        label4 = request.POST.get("label4", "")
        
        if label1:
            response = model.generate_content(''' {label1} 
                                  
            Rate the following answer from 0 to 100
            
            {Answer1}.
            
            ''')
            rate1 = to_markdown(response.text)
            # print()
            
                
        if label2:
            response = model.generate_content(''' {label2} 
                                  
            Rate the following answer from 0 to 100
            
            {Answer2}.
            
            ''')
            rate2 = to_markdown(response.text)
            
        if label3:
            response = model.generate_content(''' {label3} 
                                  
            Rate the following answer from 0 to 100
            
            {Answer3}.
            
            ''')
            rate3 = to_markdown(response.text)
            
        if label4:
            response = model.generate_content(''' {label4} 
                                  
            Rate the following answer from 0 to 100
            
            {Answer4}.
            
            ''')
            rate4 = to_markdown(response.text)
            
    # print("Answer 1:", Answer1)
    # print("Label 1:", label1)
    # print("Answer 2:", Answer2)
    # print("Label 2:", label2)
    # print("Answer 3:", Answer3)
    # print("Label 3:", label3)
    # print("Answer 4:", Answer4)
    # print("Label 4:", label4)
    
    print("Rate 1", rate1)
    print("Rate 2", rate2)
    print("Rate 3", rate3)
    print("Rate 4", rate4)
        
    context = {
        'label1': label1,
        'label2': label2,
        'label3': label3,
        'label4': label4,
        'rate1': rate1,
        'rate2': rate2,
        'rate3': rate3,
        'rate4': rate4,
    }

    return render(request, "evaluate.html", context)



def record_audio(filename, duration):
    # Record audio
    sample_rate = 44100
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait for recording to complete
    
    # Save recorded audio to file
    sf.write(filename, recording, samplerate=sample_rate)
    print("Recording saved to", filename)
    

@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES['audio_data']:
        question = request.POST.get('question')
        filename = f"media/recorded_audio{question}.wav"
        duration = 10  # Record for 20 seconds

        record_audio(filename, duration)

        return JsonResponse({'success': 'Recording successfully'})
    
    else:
        return JsonResponse({'error': 'Audio data not found!'}, status=400)

# @login_required



def extract_feature(audio_path, mfcc, chroma, mel, sample_rate):
    X, _ = librosa.load(audio_path, sr=sample_rate)  # Use the provided sample rate
    if chroma:
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))
    return result


@login_required
def prediction(request):
    if request.method == 'POST':
        model_filename = os.path.join(settings.BASE_DIR, 'speech_emotion_recognition_model.pkl')
        loaded_model = joblib.load(model_filename)

        media_path = settings.MEDIA_ROOT
        audio_paths = [os.path.join(media_path, file) for file in os.listdir(media_path) if file.endswith(('.wav', '.flac'))]

        emotions = []
        for audio_path in audio_paths:
            feature = extract_feature(audio_path, mfcc=True, chroma=True, mel=True, sample_rate=44100)
            feature = np.expand_dims(feature, axis=0)  # Add a batch dimension
            predicted_emotion = loaded_model.predict(feature)
            emotions.append(predicted_emotion[0])

        context = {
            'emotions': emotions
        }
        happy_calm_count = emotions.count('happy') + emotions.count('calm')
        if happy_calm_count >= 3:
            return render(request, 'result.html', context)        
        else:
            return render(request, 'nopass.html', context)
        
        # return render(request, 'result.html', context)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)


@login_required
def answer(request):
    if request.method == 'POST':
        about_yourself = request.POST.get('about_yourself', '')
        hear_about = request.POST.get('hear_about', '')
        company_info = request.POST.get('company_info', '')
        apply_position = request.POST.get('apply_position', '')

        # Save the user's answers to the database
        InterviewAnswer.objects.create(
            user=request.user,
            about_yourself=about_yourself,
            hear_about=hear_about,
            company_info=company_info,
            apply_position=apply_position
        )

        messages.success(request, 'Your answers have been submitted successfully!')
        return render(request, "answer.html")
        # return redirect('home')  # Redirect to the home page or any other page

    return render(request, "answer.html")


def signup(request):
    return render(request, "signup.html")

def is_valid_email(email):
    return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None

@csrf_exempt
def signup_validate(request):
    body = json.loads(request.body)
    print('body: %s' % body)
    email = body.get("email", "")
    first_name = body.get("first_name", "")
    last_name = body.get("last_name", "")
    gender = body.get("gender", "male")
    phone_number = body.get("phone_number", "")
    password = body.get("password", "")
    print('Password: %s' % password)
    print('email: %s' % email)

    if not email or not is_valid_email(email):
        result = {"success": False, "message": "Please provide a valid email"}
        return JsonResponse(result)

    if not first_name:
        result = {"success": False, "message": "Please provide your first name"}
        return JsonResponse(result)

    if not password:
        result = {"success": False, "message": "Please provide a password"}
        return JsonResponse(result)

    try:
        user = User.objects.create(username=email, email=email, password=password, 
                                        first_name=first_name, last_name=last_name,
                                        phone_number=phone_number, gender=gender)
    except IntegrityError:
        result = {"success": False, "message": "User already exists"}
        return JsonResponse(result)

    result = {"success": True, "message": "User created successfully"}
    return JsonResponse(result)

def c_login(request):
    return render(request, "login.html")




@csrf_exempt
def login_validate(request):
    body = json.loads(request.body)
    # print('body: %s' % body)
    email = body.get("email", "")
    password = body.get("password", "")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        result = {"success": False, "message": "User does not exist"}
        return JsonResponse(result)
    try:
        user = User.objects.get(email=email,password=password)
    except User.DoesNotExist:
        result = {"success": False, "message": "Invalid password"}
        return JsonResponse(result)
    # user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        result = {"success": True, "message": "Login successful"}
    else:
        result = {"success": False, "message": "Invalid password"}

    return JsonResponse(result)


@login_required
def c_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")


